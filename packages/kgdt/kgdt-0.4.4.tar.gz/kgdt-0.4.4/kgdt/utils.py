#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: isky
@Email: 19110240019@fudan.edu.cn
@Created: 2020/11/24
------------------------------------------
@Modify: 2020/11/24
------------------------------------------
@Description: Various general utility functions.
"""

import inspect
import logging
import pickle as _pickle
import traceback
import warnings
from functools import wraps

import numpy as np
import scipy.sparse
from smart_open import open

logger = logging.getLogger(__name__)


class SaveLoad:
    """Serialize/deserialize object from disk, by equipping objects with the save()/load() methods.

    Adapted from `gensim/utils.py
    <https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/utils.py>`_.

    Warnings
    --------
    This uses pickle internally (among other techniques), so objects must not contain unpicklable attributes
    such as lambda functions etc.

    """

    @classmethod
    def load(cls, fname, mmap=None):
        """Load an object previously saved using :meth:`~gensim.utils.SaveLoad.save` from a file.

        Parameters
        ----------
        fname : str
            Path to file that contains needed object.
        mmap : str, optional
            Memory-map option.  If the object was saved with large arrays stored separately, you can load these arrays
            via mmap (shared memory) using `mmap='r'.
            If the file being loaded is compressed (either '.gz' or '.bz2'), then `mmap=None` **must be** set.

        See Also
        --------
        :meth:`~gensim.utils.SaveLoad.save`
            Save object to file.

        Returns
        -------
        object
            Object loaded from `fname`.

        Raises
        ------
        AttributeError
            When called on an object instance instead of class (this is a class method).

        """
        logger.info("loading %s object from %s", cls.__name__, fname)

        compress, subname = SaveLoad._adapt_by_suffix(fname)

        obj = unpickle(fname)
        obj._load_specials(fname, mmap, compress, subname)
        logger.info("loaded %s", fname)
        return obj

    def _load_specials(self, fname, mmap, compress, subname):
        """Load attributes that were stored separately, and give them the same opportunity
        to recursively load using the :class:`~gensim.utils.SaveLoad` interface.

        Parameters
        ----------
        fname : str
            Input file path.
        mmap :  {None, ‘r+’, ‘r’, ‘w+’, ‘c’}
            Memory-map options. See `numpy.load(mmap_mode)
            <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.load.html>`_.
        compress : bool
            Is the input file compressed?
        subname : str
            Attribute name. Set automatically during recursive processing.

        """

        def mmap_error(obj, filename):
            return IOError(
                'Cannot mmap compressed object %s in file %s. ' % (obj, filename)
                + 'Use `load(fname, mmap=None)` or uncompress files manually.'
            )

        for attrib in getattr(self, '__recursive_saveloads', []):
            cfname = '.'.join((fname, attrib))
            logger.info("loading %s recursively from %s.* with mmap=%s", attrib, cfname, mmap)
            getattr(self, attrib)._load_specials(cfname, mmap, compress, subname)

        for attrib in getattr(self, '__numpys', []):
            logger.info("loading %s from %s with mmap=%s", attrib, subname(fname, attrib), mmap)

            if compress:
                if mmap:
                    raise mmap_error(attrib, subname(fname, attrib))

                val = np.load(subname(fname, attrib))['val']
            else:
                val = np.load(subname(fname, attrib), mmap_mode=mmap)

            setattr(self, attrib, val)

        for attrib in getattr(self, '__scipys', []):
            logger.info("loading %s from %s with mmap=%s", attrib, subname(fname, attrib), mmap)
            sparse = unpickle(subname(fname, attrib))
            if compress:
                if mmap:
                    raise mmap_error(attrib, subname(fname, attrib))

                with np.load(subname(fname, attrib, 'sparse')) as f:
                    sparse.data = f['data']
                    sparse.indptr = f['indptr']
                    sparse.indices = f['indices']
            else:
                sparse.data = np.load(subname(fname, attrib, 'data'), mmap_mode=mmap)
                sparse.indptr = np.load(subname(fname, attrib, 'indptr'), mmap_mode=mmap)
                sparse.indices = np.load(subname(fname, attrib, 'indices'), mmap_mode=mmap)

            setattr(self, attrib, sparse)

        for attrib in getattr(self, '__ignoreds', []):
            logger.info("setting ignored attribute %s to None", attrib)
            setattr(self, attrib, None)

    @staticmethod
    def _adapt_by_suffix(fname):
        """Get compress setting and filename for numpy file compression.

        Parameters
        ----------
        fname : str
            Input filename.

        Returns
        -------
        (bool, function)
            First argument will be True if `fname` compressed.

        """
        compress, suffix = (True, 'npz') if fname.endswith('.gz') or fname.endswith('.bz2') else (False, 'npy')
        return compress, lambda *args: '.'.join(args + (suffix,))

    def _smart_save(self, fname, separately=None, sep_limit=10 * 1024 ** 2, ignore=frozenset(), pickle_protocol=2):
        """Save the object to a file. Used internally by :meth:`gensim.utils.SaveLoad.save()`.

        Parameters
        ----------
        fname : str
            Path to file.
        separately : list, optional
            Iterable of attributes than need to store distinctly.
        sep_limit : int, optional
            Limit for separation.
        ignore : frozenset, optional
            Attributes that shouldn't be store.
        pickle_protocol : int, optional
            Protocol number for pickle.

        Notes
        -----
        If `separately` is None, automatically detect large numpy/scipy.sparse arrays in the object being stored,
        and store them into separate files. This avoids pickle memory errors and allows mmap'ing large arrays back
        on load efficiently.

        You can also set `separately` manually, in which case it must be a list of attribute names to be stored
        in separate files. The automatic check is not performed in this case.

        """
        logger.info("saving %s under %s, separately %s", self, fname, separately)

        compress, subname = SaveLoad._adapt_by_suffix(fname)

        restores = self._save_specials(fname, separately, sep_limit, ignore, pickle_protocol,
                                       compress, subname)
        try:
            pickle(self, fname, protocol=pickle_protocol)
        finally:
            # restore attribs handled specially
            for obj, asides in restores:
                for attrib, val in asides.items():
                    setattr(obj, attrib, val)
        logger.info("saved %s", fname)

    def _save_specials(self, fname, separately, sep_limit, ignore, pickle_protocol, compress, subname):
        """Save aside any attributes that need to be handled separately, including
        by recursion any attributes that are themselves :class:`~gensim.utils.SaveLoad` instances.

        Parameters
        ----------
        fname : str
            Output filename.
        separately : list or None
            List of attributes to store separately.
        sep_limit : int
            Don't store arrays smaller than this separately. In bytes.
        ignore : iterable of str
            Attributes that shouldn't be stored at all.
        pickle_protocol : int
            Protocol number for pickle.
        compress : bool
            If True - compress output with :func:`numpy.savez_compressed`.
        subname : function
            Produced by :meth:`~gensim.utils.SaveLoad._adapt_by_suffix`

        Returns
        -------
        list of (obj, {attrib: value, ...})
            Settings that the caller should use to restore each object's attributes that were set aside
            during the default :func:`~gensim.utils.pickle`.

        """
        asides = {}
        sparse_matrices = (scipy.sparse.csr_matrix, scipy.sparse.csc_matrix)
        if separately is None:
            separately = []
            for attrib, val in self.__dict__.items():
                if isinstance(val, np.ndarray) and val.size >= sep_limit:
                    separately.append(attrib)
                elif isinstance(val, sparse_matrices) and val.nnz >= sep_limit:
                    separately.append(attrib)

        # whatever's in `separately` or `ignore` at this point won't get pickled
        for attrib in separately + list(ignore):
            if hasattr(self, attrib):
                asides[attrib] = getattr(self, attrib)
                delattr(self, attrib)

        recursive_saveloads = []
        restores = []
        for attrib, val in self.__dict__.items():
            if hasattr(val, '_save_specials'):  # better than 'isinstance(val, SaveLoad)' if IPython reloading
                recursive_saveloads.append(attrib)
                cfname = '.'.join((fname, attrib))
                restores.extend(val._save_specials(cfname, None, sep_limit, ignore, pickle_protocol, compress, subname))

        try:
            numpys, scipys, ignoreds = [], [], []
            for attrib, val in asides.items():
                if isinstance(val, np.ndarray) and attrib not in ignore:
                    numpys.append(attrib)
                    logger.info("storing np array '%s' to %s", attrib, subname(fname, attrib))

                    if compress:
                        np.savez_compressed(subname(fname, attrib), val=np.ascontiguousarray(val))
                    else:
                        np.save(subname(fname, attrib), np.ascontiguousarray(val))

                elif isinstance(val, (scipy.sparse.csr_matrix, scipy.sparse.csc_matrix)) and attrib not in ignore:
                    scipys.append(attrib)
                    logger.info("storing scipy.sparse array '%s' under %s", attrib, subname(fname, attrib))

                    if compress:
                        np.savez_compressed(
                            subname(fname, attrib, 'sparse'),
                            data=val.data,
                            indptr=val.indptr,
                            indices=val.indices
                        )
                    else:
                        np.save(subname(fname, attrib, 'data'), val.data)
                        np.save(subname(fname, attrib, 'indptr'), val.indptr)
                        np.save(subname(fname, attrib, 'indices'), val.indices)

                    data, indptr, indices = val.data, val.indptr, val.indices
                    val.data, val.indptr, val.indices = None, None, None

                    try:
                        # store array-less object
                        pickle(val, subname(fname, attrib), protocol=pickle_protocol)
                    finally:
                        val.data, val.indptr, val.indices = data, indptr, indices
                else:
                    logger.info("not storing attribute %s", attrib)
                    ignoreds.append(attrib)

            self.__dict__['__numpys'] = numpys
            self.__dict__['__scipys'] = scipys
            self.__dict__['__ignoreds'] = ignoreds
            self.__dict__['__recursive_saveloads'] = recursive_saveloads
        except Exception:
            # restore the attributes if exception-interrupted
            for attrib, val in asides.items():
                setattr(self, attrib, val)
            raise
        return restores + [(self, asides)]

    def save(self, fname_or_handle, separately=None, sep_limit=10 * 1024 ** 2, ignore=frozenset(), pickle_protocol=2):
        """Save the object to a file.

        Parameters
        ----------
        fname_or_handle : str or file-like
            Path to output file or already opened file-like object. If the object is a file handle,
            no special array handling will be performed, all attributes will be saved to the same file.
        separately : list of str or None, optional
            If None, automatically detect large numpy/scipy.sparse arrays in the object being stored, and store
            them into separate files. This prevent memory errors for large objects, and also allows
            `memory-mapping <https://en.wikipedia.org/wiki/Mmap>`_ the large arrays for efficient
            loading and sharing the large arrays in RAM between multiple processes.

            If list of str: store these attributes into separate files. The automated size check
            is not performed in this case.
        sep_limit : int, optional
            Don't store arrays smaller than this separately. In bytes.
        ignore : frozenset of str, optional
            Attributes that shouldn't be stored at all.
        pickle_protocol : int, optional
            Protocol number for pickle.

        See Also
        --------
        :meth:`~gensim.utils.SaveLoad.load`
            Load object from file.

        """
        try:
            _pickle.dump(self, fname_or_handle, protocol=pickle_protocol)
            logger.info("saved %s object", self.__class__.__name__)
        except TypeError:  # `fname_or_handle` does not have write attribute
            self._smart_save(fname_or_handle, separately, sep_limit, ignore, pickle_protocol=pickle_protocol)


def pickle(obj, fname, protocol=2):
    """Pickle object `obj` to file `fname`, using smart_open so that `fname` can be on S3, HDFS, compressed etc.

    Parameters
    ----------
    obj : object
        Any python object.
    fname : str
        Path to pickle file.
    protocol : int, optional
        Pickle protocol number. Default is 2 in order to support compatibility across python 2.x and 3.x.

    """
    with open(fname, 'wb') as fout:  # 'b' for binary, needed on Windows
        _pickle.dump(obj, fout, protocol=protocol)


def unpickle(fname):
    """Load object from `fname`, using smart_open so that `fname` can be on S3, HDFS, compressed etc.

    Parameters
    ----------
    fname : str
        Path to pickle file.

    Returns
    -------
    object
        Python object loaded from `fname`.

    """
    with open(fname, 'rb') as f:
        return _pickle.load(f, encoding='latin1')  # needed because loading from S3 doesn't support readline()


def deprecated(reason):
    """Decorator to mark functions as deprecated.

    Calling a decorated function will result in a warning being emitted, using warnings.warn.
    Adapted from https://stackoverflow.com/a/40301488/8001386.

    Parameters
    ----------
    reason : str
        Reason of deprecation.

    Returns
    -------
    function
        Decorated function

    """
    if isinstance(reason, str):
        def decorator(func):
            fmt = "Call to deprecated `{name}` ({reason})."

            @wraps(func)
            def new_func1(*args, **kwargs):
                warnings.warn(
                    fmt.format(name=func.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                return func(*args, **kwargs)

            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        func = reason
        fmt = "Call to deprecated `{name}`."

        @wraps(func)
        def new_func2(*args, **kwargs):
            warnings.warn(
                fmt.format(name=func.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))


def catch_exception(function):
    """
    a decorator to catch exception and print it.
    :return:
    """
    # todo: make this print as the parameter of the decorator
    def wrapped(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()

    return wrapped

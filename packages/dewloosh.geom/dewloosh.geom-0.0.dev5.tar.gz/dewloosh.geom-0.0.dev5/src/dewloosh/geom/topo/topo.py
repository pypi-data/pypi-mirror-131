# -*- coding: utf-8 -*-
from dewloosh.math.linalg.sparse.csr import csr_matrix
from dewloosh.math.linalg.sparse.jaggedarray import JaggedArray
from dewloosh.math.arraysetops import unique2d
from dewloosh.math.array import count_cols
import numpy as np
from numpy import ndarray
from numba import njit, prange
import networkx as nx
from typing import Union, Dict, List, Tuple
from awkward import Array as akarray
from scipy.sparse import csr_matrix as csr_scipy
__cache = True


__all__ = ['is_regular', 'regularize', 'count_cells_at_nodes', 'cells_at_nodes',
           'nodal_adjacency', 'unique_topo_data']


TopoLike = Union[ndarray, JaggedArray]
DoL = Dict[int, List[int]]


def is_regular(topo: TopoLike) -> bool:
    """Returns True if the topology is regular, in the meaning
    that the smallest node index is zero, and every integer
    is represented up to the maximum index."""
    if isinstance(topo, ndarray):
        return topo.min() == 0 and len(np.unique(topo)) == topo.max() + 1
    elif isinstance(topo, akarray):
        return np.min(topo) == 0 and len(unique2d(topo)) == np.max(topo) + 1
    else:
        raise NotImplementedError


def regularize(topo: TopoLike) -> Tuple[TopoLike, ndarray]:
    """Returns a regularized topology and the unique indices.
    The returned topology array contain indices of the unique
    array."""
    if isinstance(topo, ndarray):
        unique, regular = np.unique(topo, return_inverse=True)
        regular = regular.reshape(topo.shape)
        return regular, unique
    elif isinstance(topo, akarray):
        unique, regular = unique2d(topo, return_inverse=True)
        return regular, unique
    else:
        raise NotImplementedError


@njit(nogil=True, parallel=False, fastmath=True, cache=__cache)
def _count_cells_at_nodes_reg_np_(topo: ndarray) -> ndarray:
    """Assumes a regular topology. Returns an array."""
    nE, nNE = topo.shape
    nN = topo.max() + 1
    count = np.zeros((nN), dtype=topo.dtype)
    for iE in prange(nE):
        for jNE in prange(nNE):
            count[topo[iE, jNE]] += 1
    return count


@njit(nogil=True, parallel=False, fastmath=True, cache=__cache)
def _count_cells_at_nodes_reg_ak_(topo: akarray) -> ndarray:
    """Assumes a regular topology. Returns an array."""
    ncols = count_cols(topo)
    nE = len(ncols)
    nN = np.max(topo) + 1
    count = np.zeros((nN), dtype=topo.dtype)
    for iE in prange(nE):
        for jNE in prange(ncols[iE]):
            count[topo[iE, jNE]] += 1
    return count


@njit(nogil=True, parallel=False, fastmath=True, cache=__cache)
def _count_cells_at_nodes_np_(topo: ndarray, nodeIDs: ndarray) -> Dict[int, int]:
    """Returns a dict{int : int} for the nodes in `nideIDs`.
    Assumes an irregular topology. The array `topo` must contain 
    indices relative to `nodeIDs`. If the topology is regular, 
    `nodeIDs == np.arange(topo.max() + 1)` is `True`."""
    nE, nNE = topo.shape
    count = dict()
    for i in range(len(nodeIDs)):
        count[nodeIDs[i]] = 0
    for iE in prange(nE):
        for jNE in prange(nNE):
            count[nodeIDs[topo[iE, jNE]]] += 1
    return count


@njit(nogil=True, parallel=False, fastmath=True, cache=__cache)
def _count_cells_at_nodes_ak_(topo: akarray, nodeIDs: ndarray) -> Dict[int, int]:
    """Returns a dict{int : int} for the nodes in `nideIDs`.
    Assumes an irregular topology. The array `topo` must contain 
    indices relative to `nodeIDs`. If the topology is regular, 
    `nodeIDs == np.arange(topo.max() + 1)` is `True`."""
    ncols = count_cols(topo)
    nE = len(ncols)
    count = dict()
    for i in range(len(nodeIDs)):
        count[nodeIDs[i]] = 0
    for iE in prange(nE):
        for jNE in prange(ncols[iE]):
            count[nodeIDs[topo[iE, jNE]]] += 1
    return count


def count_cells_at_nodes(topo: TopoLike, regular=False):
    """
    Returns an array or a discionary, that counts connecting 
    elements at the nodes of a mesh.

    Parameters
    ----------
    topo : TopoLike
        2d numpy or awkward array describing the topoogy of a mesh.

    Returns
    -------
    count : np.ndarray(nN) or dict[int : int]
        Number of connecting elements for each node in a mesh.
    """
    if not regular:
        if isinstance(topo, ndarray):
            topo, nodeIDs = regularize(topo)
            return _count_cells_at_nodes_np_(topo, nodeIDs)
        elif isinstance(topo, akarray):
            topo, nodeIDs = regularize(topo)
            return _count_cells_at_nodes_ak_(topo, nodeIDs)
        else:
            raise NotImplementedError
    else:
        if isinstance(topo, ndarray):
            return _count_cells_at_nodes_reg_np_(topo)
        elif isinstance(topo, akarray):
            return _count_cells_at_nodes_reg_ak_(topo)
        else:
            raise NotImplementedError


def cells_at_nodes(topo: TopoLike, *args, frmt=None, assume_regular=False,
                   cellIDs=None, return_counts=False, **kwargs):
    """ Returns data about element connectivity at the nodes of a mesh.

    Parameters
    ----------
    topo : numpy.ndarray array or JaggedArray
        A 2d array (either jagged or not) representing topological data of a mesh.

    frmt : str
        A string specifying the output format. Valid options are
        'jagged', 'csr', 'scipy-csr' and 'dicts'. 
        See below for the details on the returned object.   

    return_counts : bool
        Wether to return the numbers of connecting elements at the nodes
        as a numpy array. If format is 'raw', the
        counts are always returned irrelevant to this option.

    assume_regular : bool
        If the topology is regular, you can gain some speed with providing
        it as `True`. Default is `False`.

    cellIDs : numpy.ndarray
        Indices of the cells in `topo`. If nor `None`, format must be 'dicts'.
        Default is `None`.

    Returns
    -------
    If `return_counts` is `True`, the number of connecting elements for
    each node is returned as either a numpy array (if `cellIDs` is `None`) 
    or a dictionary (if `cellIDs` is not `None`). If format is 'raw', the
    counts are always returned.

    if frmt == None
        counts : np.ndarray(nN) - numbers of connecting elements
        ereg : np.ndarray(nN, nmax) - indices of connecting elements
        nreg : np.ndarray(nN, nmax) - node indices with respect to the
                                      connecting elements
        where
            nN - is the number of nodes,
            nmax - is the maximum number of elements that meet at a node, that is
                count.max()  
    elif frmt == 'csr'
        counts(optionally) : np.ndarray(nN) - number of connecting elements
        csr : csr_matrix - sparse matrix in a numba-jittable csr format.
                           Column indices denote element indices, values
                           have the meaning of element node locations.                       
    elif frmt == 'scipy-csr'
        counts(optionally) : np.ndarray(nN) - number of connecting elements
        csr : csr_matrix - An instance of scipy.linalg.sparse.csr_matrix.
                           Column indices denote element indices, values
                           have the meaning of element node locations.
    elif frmt == 'dicts'
        counts(optionally) : np.ndarray(nN) - number of connecting elements
        ereg : numba Dict(int : int[:]) - indices of elements for each node
                                          index
        nreg : numba Dict(int : int[:]) - local indices of nodes in the
                                          connecting elements   
    elif frmt == 'jagged'
        counts(optionally) : np.ndarray(nN) - number of connecting elements
        ereg : JaggedArray - indices of elements for each node index
        nreg : JaggedArray - local indices of nodes in the connecting elements   

    """
    if cellIDs is not None:
        assert frmt == 'dicts', "If `cellIDs` is not None,"\
            + " output format must be 'dicts'."

    if not assume_regular:
        if is_regular(topo):
            nodeIDs = None
        else:
            topo, nodeIDs = regularize(topo)
    else:
        nodeIDs = None

    if nodeIDs is not None:
        assert frmt == 'dicts', "Only the format 'dicts' supports an irregular input!"

    if isinstance(topo, ndarray):
        counts, ereg, nreg = _cells_at_nodes_reg_np_(topo)
    elif isinstance(topo, akarray):
        counts, ereg, nreg = _cells_at_nodes_reg_ak_(topo)
    else:
        raise NotImplementedError

    frmt = '' if frmt is None else frmt

    if frmt in ['csr', 'csr-scipy']:
        data, indices, indptr, shape = \
            _nodal_cell_data_to_spdata_(counts, ereg, nreg)
        csr = csr_matrix(data=data, indices=indices,
                         indptr=indptr, shape=shape)
        if frmt == 'csr':
            csr = csr_matrix(data=data, indices=indices,
                             indptr=indptr, shape=shape)
        else:
            csr = csr_scipy((data, indices, indptr), shape=shape)
        if return_counts:
            return counts, csr
        return csr
    elif frmt == 'dicts':
        cellIDs = np.arange(len(topo)) if cellIDs is None else cellIDs
        nodeIDs = np.arange(len(counts)) if nodeIDs is None else nodeIDs
        ereg, nreg = _nodal_cell_data_to_dicts_(
            counts, ereg, nreg, cellIDs, nodeIDs)
        if return_counts:
            return counts, ereg, nreg
        return ereg, nreg
    elif frmt == 'jagged':
        data, indices, indptr, shape = \
            _nodal_cell_data_to_spdata_(counts, ereg, nreg)
        ereg = JaggedArray(indices, cuts=counts)
        nreg = JaggedArray(data, cuts=counts)
        if return_counts:
            return counts, ereg, nreg
        return ereg, nreg

    return counts, ereg, nreg


@njit(nogil=True, cache=__cache)
def _cells_at_nodes_reg_np_(topo: ndarray):
    """Returns arrays. Assumes a regular topology."""
    nE, nNE = topo.shape
    nN = topo.max() + 1
    count = _count_cells_at_nodes_reg_np_(topo)
    cmax = count.max()
    ereg = np.zeros((nN, cmax), dtype=topo.dtype)
    nreg = np.zeros((nN, cmax), dtype=topo.dtype)
    count[:] = 0
    for iE in range(nE):
        for jNE in range(nNE):
            ereg[topo[iE, jNE], count[topo[iE, jNE]]] = iE
            nreg[topo[iE, jNE], count[topo[iE, jNE]]] = jNE
            count[topo[iE, jNE]] += 1
    return count, ereg, nreg


@njit(nogil=True, cache=__cache)
def _cells_at_nodes_reg_ak_(topo: akarray):
    """Returns arrays. Assumes a regular topology."""
    ncols = count_cols(topo)
    nE = len(ncols)
    count = _count_cells_at_nodes_reg_ak_(topo)
    nN = np.max(topo) + 1
    cmax = count.max()
    ereg = np.zeros((nN, cmax), dtype=topo.dtype)
    nreg = np.zeros((nN, cmax), dtype=topo.dtype)
    count[:] = 0
    for iE in range(nE):
        for jNE in range(ncols[iE]):
            ereg[topo[iE, jNE], count[topo[iE, jNE]]] = iE
            nreg[topo[iE, jNE], count[topo[iE, jNE]]] = jNE
            count[topo[iE, jNE]] += 1
    return count, ereg, nreg


@njit(nogil=True, cache=__cache)
def _nodal_cell_data_to_dicts_(count: ndarray, ereg: ndarray,
                               nreg: ndarray, cellIDs: ndarray,
                               nodeIDs: ndarray) -> Tuple[Dict, Dict]:
    ereg_d = dict()
    nreg_d = dict()
    for i in range(len(count)):
        ereg_d[nodeIDs[i]] = cellIDs[ereg[i, : count[i]]]
        nreg_d[nodeIDs[i]] = nreg[i, : count[i]]
    return ereg_d, nreg_d


@njit(nogil=True, parallel=True, cache=__cache)
def _nodal_cell_data_to_spdata_(count: np.ndarray, ereg: np.ndarray,
                                nreg: np.ndarray) -> tuple:
    nE = ereg.max() + 1
    nN = len(count)
    N = np.sum(count)
    indices = np.zeros(N, dtype=count.dtype)
    data = np.zeros(N, dtype=count.dtype)
    indptr = np.zeros(nN+1, dtype=count.dtype)
    indptr[1:] = np.cumsum(count)
    for i in prange(nN):
        indices[indptr[i]: indptr[i+1]] = ereg[i, : count[i]]
        data[indptr[i]: indptr[i+1]] = nreg[i, : count[i]]
    shape = (nN, nE)
    return data, indices, indptr, shape


@njit(nogil=True, cache=__cache)
def _nodal_adjacency_as_dol_np_(topo: ndarray, ereg: DoL) -> DoL:
    """Returns nodal adjacency as a dictionary of lists."""
    res = dict()
    for iP in ereg:
        res[iP] = np.unique(topo[ereg[iP], :])
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def _subtopo_1d_(topo1d: ndarray, cuts: ndarray, inds: ndarray,
                 indptr: ndarray) -> ndarray:
    nN = np.sum(cuts[inds])
    nE = len(inds)
    subindptr = np.zeros(nN+1, dtype=cuts.dtype)
    subindptr[1:] = np.cumsum(cuts[inds])
    subtopo1d = np.zeros(nN, dtype=topo1d.dtype)
    for iE in prange(nE):
        subtopo1d[subindptr[iE]: subindptr[iE+1]] = \
            topo1d[indptr[inds[iE]]: indptr[inds[iE]+1]]
    return subtopo1d


@njit(nogil=True, cache=__cache)
def _nodal_adjacency_as_dol_ak_(topo1d: ndarray, cuts: ndarray, ereg: DoL) -> DoL:
    """Returns nodal adjacency as a dictionary of lists."""
    res = dict()
    nN = len(cuts)
    indptr = np.zeros(nN+1, dtype=cuts.dtype)
    indptr[1:] = np.cumsum(cuts)
    for iP in ereg:
        res[iP] = np.unique(_subtopo_1d_(topo1d, cuts, ereg[iP], indptr))
    return res


@njit(nogil=True, parallel=False, fastmath=False, cache=__cache)
def dol_keys(dol: DoL) -> ndarray:
    nD = len(dol)
    res = np.zeros(nD, dtype=np.int64)
    c = 0
    for i in dol:
        res[c] = i
        c += 1
    return res


@njit(nogil=True, parallel=True, cache=__cache)
def dol_to_jagged_data(dol: DoL) -> Tuple[ndarray, ndarray]:
    nD = len(dol)
    keys = dol_keys(dol)
    widths = np.zeros(nD, dtype=np.int64)
    for i in prange(nD):
        widths[i] = len(dol[keys[i]])
    indptr = np.zeros(nD+1, dtype=np.int64)
    indptr[1:] = np.cumsum(widths)
    N = np.sum(widths)
    data1d = np.zeros(N, dtype=np.int64)
    for i in prange(nD):
        data1d[indptr[i]: indptr[i+1]] = dol[keys[i]]
    return widths, data1d


def nodal_adjacency(topo: TopoLike, *args, frmt=None, assume_regular=False, **kwargs):
    """Returns nodal adjacency information of a mesh.

    Parameters
    ----------
    topo : numpy.ndarray array or JaggedArray
        A 2d array (either jagged or not) representing topological data of a mesh.

    frmt : str
        A string specifying the output format. Valid options are
        'jagged', 'csr' and 'scipy-csr'. See below for the details on the 
        returned object.

    assume_regular : bool
        If the topology is regular, you can gain some speed with providing
        it as `True`. Default is `False`.
        
    Notes
    -----
    A node is adjacent to itself.

    Returns
    -------
    if frmt == None
        A dictionary of numpy arrays for each node.
    elif frmt == 'csr'
        csr_matrix - A sparse matrix in a numba-jittable csr format.
    elif frmt == 'scipy-csr'
        An instance of scipy.linalg.sparse.csr_matrix.
    elif frmt == 'nx'
        A networkx Graph.
    elif frmt == 'jagged'
        A JaggedArray instance.

    """
    frmt = '' if frmt is None else frmt
    ereg, _ = cells_at_nodes(topo, frmt='dicts', assume_regular=assume_regular)
    if isinstance(topo, ndarray):
        dol = _nodal_adjacency_as_dol_np_(topo, ereg)
    elif isinstance(topo, akarray):
        cuts, topo1d = JaggedArray(topo).flatten(return_cuts=True)
        dol = _nodal_adjacency_as_dol_ak_(topo1d.to_numpy(), cuts, ereg)
    if frmt == 'nx':
        return nx.from_dict_of_lists(dol)
    elif frmt == 'scipy-csr':
        G = nx.from_dict_of_lists(dol)
        return nx.to_scipy_sparse_matrix(G).tocsr()
    elif frmt == 'csr':
        G = nx.from_dict_of_lists(dol)
        csr = nx.to_scipy_sparse_matrix(G).tocsr()
        return csr_matrix(csr)
    elif frmt == 'jagged':
        cuts, data1d = dol_to_jagged_data(dol)
        return JaggedArray(data1d, cuts=cuts)
    return dol


def unique_topo_data(topo3d: TopoLike):
    """Returns information about unique topological elements
    of a mesh. It can be used to return unique lines of a 2d
    mesh, unique faces of a 3d mesh, etc.

    Parameters
    ----------
        topo : numpy.ndarray 
            Topology array.

    Returns
    -------
    numpy.ndarray
        Integer array of indices, representing unique elements.

    numpy.ndarray
        Indices of the unique array, that can be used to 
        reconstruct `topo`.
    """
    if isinstance(topo3d, ndarray):
        nE, nD, nN = topo3d.shape
        topo3d = topo3d.reshape((nE * nD, nN))
        topo3d = np.sort(topo3d, axis=1)
        topo3d, topoIDs = np.unique(topo3d, axis=0, return_inverse=True)
        topoIDs = topoIDs.reshape((nE, nD))
        return topo3d, topoIDs
    elif isinstance(topo3d, JaggedArray):
        raise NotImplementedError


"""
def unique_lines(lines : np.ndarray):
    # ! IN PROGRESS
    raise NotImplementedError
    nE, nL, nNL = lines.shape
    lines = lines.reshape((nE * nL, nNL))
    lines = np.sort(lines, axis=1)
    lines, lineIDs = np.unique(lines[:, [0, -1]], axis=0, return_inverse=True)
    lineIDs = lineIDs.reshape((nE, nL))
    return lines, lineIDs


def unique_lines_of_areas(topo : np.ndarray, lpath : np.ndarray):
    # ! IN PROGRESS
    raise NotImplementedError
    return unique_lines(lines_of_areas_njit(topo, lpath))


@njit(nogil=True, parallel=True, cache=__cache)
def lines_of_areas_njit(topo : np.ndarray, lpaths : np.ndarray):
    # ! CHECK
    nE = topo.shape[0]
    nL, nNL = lpaths.shape
    lines = np.zeros((nE, nL, nNL), dtype=topo.dtype)
    for iE in prange(nE):
        for jL in prange(nL):
            for kL in prange(nNL):
                lines[iE, jL, kL] = topo[iE, lpaths[jL, kL]]
    return lines
"""

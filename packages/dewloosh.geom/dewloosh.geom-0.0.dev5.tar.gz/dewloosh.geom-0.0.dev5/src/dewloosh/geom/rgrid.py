# -*- coding: utf-8 -*-
import numpy as np
from numba import njit, prange
from dewloosh.geom.topo.tr import transform_topo
__cache = True


__all__ = ['grid', 'gridQ4', 'gridQ9', 'gridH8', 'gridH27']


def grid(*args, size=None, shape=None, eshape=None, origo=None, start=0,
          bins=None, **kwargs):
    nDime = len(size)
    if eshape is None:
        eshape = np.full(nDime, 2, dtype=int)
    elif isinstance(eshape, str):
        if eshape == 'Q4':
            return gridQ4(*args, size=size, shape=shape, origo=origo,
                           start=start, **kwargs)
        elif eshape == 'Q9':
            return gridQ9(*args, size=size, shape=shape, origo=origo,
                           start=start, **kwargs)
        elif eshape == 'H8':
            return gridH8(*args, size=size, shape=shape, origo=origo,
                           start=start, **kwargs)
        elif eshape == 'H27':
            return gridH27(*args, size=size, shape=shape, origo=origo,
                            start=start, **kwargs)
        else:
            raise NotImplementedError
    if origo is None:
        origo = np.zeros(nDime)

    if isinstance(bins, np.ndarray):
        if bins.shape[0] == 3:
            coords, topo = grid_3d_bins(bins[0], bins[1], bins[2],
                                        eshape, origo, start)
        else:
            # !TODO : fix rgrid_2d_bins
            raise NotImplementedError
    else:
        if shape is None:
            shape = np.full(nDime, 1, dtype=int)
        coords, topo = rgridMT(size, shape, eshape, origo, start)

    return coords, topo


def gridQ4(*args, **kwargs):
    coords, topo = grid(*args, eshape=(2, 2), **kwargs)
    path = np.array([0, 2, 3, 1], dtype=int)
    return coords, transform_topo(topo, path)


def gridQ9(*args, **kwargs):
    coords, topo = grid(*args, eshape=(3, 3), **kwargs)
    path = np.array([0, 6, 8, 2, 3, 7, 5, 1, 4], dtype=int)
    return coords, transform_topo(topo, path)


def gridH8(*args, **kwargs):
    coords, topo = grid(*args, eshape=(2, 2, 2), **kwargs)
    path = np.array([0, 4, 6, 2, 1, 5, 7, 3], dtype=int)
    return coords, transform_topo(topo, path)


def gridH27(*args, **kwargs):
    coords, topo = grid(*args, eshape=(3, 3, 3), **kwargs)
    path = np.array([0, 18, 24, 6, 2, 20, 26, 8, 9, 21, 15, 3, 11, 23, 17, 5,
                     1, 19, 25, 7, 4, 22, 10, 16, 12, 14, 13], dtype=int)
    return coords, transform_topo(topo, path)


@njit(nogil=True, cache=__cache)
def rgridST(size, shape, eshape, origo, start=0):
    nDime = len(size)

    if nDime == 1:
        lX = size
        ndivX = shape
        nNodeX = eshape
        nX = ndivX * (nNodeX - 1) + 1
        dX = lX / ndivX
        ddX = dX / (nNodeX - 1)
        numCell = ndivX
        numPoin = nX
        numNode = nNodeX
    elif nDime == 2:
        lX, lY = size
        ndivX, ndivY = shape
        nNodeX, nNodeY = eshape
        nX = ndivX * (nNodeX - 1) + 1
        nY = ndivY * (nNodeY - 1) + 1
        dX = lX / ndivX
        dY = lY / ndivY
        ddX = dX / (nNodeX - 1)
        ddY = dY / (nNodeY - 1)
        numCell = ndivX * ndivY
        numPoin = nX * nY
        numNode = nNodeX * nNodeY
    elif nDime == 3:
        lX, lY, lZ = size
        ndivX, ndivY, ndivZ = shape
        nNodeX, nNodeY, nNodeZ = eshape
        nX = ndivX * (nNodeX - 1) + 1
        nY = ndivY * (nNodeY - 1) + 1
        nZ = ndivZ * (nNodeZ - 1) + 1
        dX = lX / ndivX
        dY = lY / ndivY
        dZ = lZ / ndivZ
        ddX = dX / (nNodeX - 1)
        ddY = dY / (nNodeY - 1)
        ddZ = dZ / (nNodeZ - 1)
        numCell = ndivY * ndivX * ndivZ
        numPoin = nX * nY * nZ
        numNode = nNodeX * nNodeY * nNodeZ

    # set up nodal coordinates
    coords = np.zeros((numPoin, nDime))
    topo = np.zeros((numCell, numNode), dtype=int)
    elem = -1
    if nDime == 1:
        for i in range(1, ndivX+1):
            elem += 1
            ne = -1
            n = (nNodeX-1) * (i-1)
            for j in range(1, nNodeX+1):
                n += 1
                coords[n-1, 0] = origo + dX * (i-1) + ddX * (j-1)
                ne += 1
                topo[elem, ne] = n
    elif nDime == 2:
        for i in range(1, ndivX + 1):
            for j in range(1, ndivY + 1):
                elem += 1
                ne = -1
                for k in range(1, nNodeX + 1):
                    for m in range(1, nNodeY + 1):
                        n = ((nNodeX - 1) * (i - 1) + k - 1) * nY + \
                            (nNodeY - 1) * (j - 1) + m
                        coords[n - 1, 0] = origo[0] + dX * (i - 1) + \
                            ddX * (k - 1)
                        coords[n - 1, 1] = origo[1] + dY * (j - 1) + \
                            ddY * (m - 1)
                        ne += 1
                        topo[elem, ne] = n
    elif nDime == 3:
        for i in range(1, ndivX+1):
            for j in range(1, ndivY+1):
                for k in range(1, ndivZ+1):
                    elem += 1
                    ne = -1
                    for m in range(1, nNodeX+1):
                        for q in range(1, nNodeY+1):
                            for p in range(1, nNodeZ+1):
                                n = (((nNodeX-1)*(i-1) + m-1)*nY +
                                     (nNodeY-1)*(j-1) + q-1)*nZ + \
                                    (nNodeZ-1)*(k-1) + p
                                coords[n-1, 0] = origo[0] + dX * (i-1) + \
                                    ddX * (m-1)
                                coords[n-1, 1] = origo[1] + dY * (j-1) + \
                                    ddY * (q-1)
                                coords[n-1, 2] = origo[2] + dZ * (k-1) + \
                                    ddZ * (p-1)
                                ne += 1
                                topo[elem, ne] = n
    start -= 1
    return coords, topo + start


@njit(nogil=True, parallel=True, fastmath=True, cache=__cache)
def rgridMT(size, shape, eshape, origo, start=0):
    nDime = len(size)
    if nDime == 1:
        lX = size[0]
        ndivX = shape
        nNodeX = eshape
        nX = ndivX * (nNodeX - 1) + 1
        dX = lX / ndivX
        ddX = dX / (nNodeX - 1)
        numCell = ndivX
        numPoin = nX
        numNode = nNodeX
    elif nDime == 2:
        lX, lY = size
        ndivX, ndivY = shape
        nNodeX, nNodeY = eshape
        nX = ndivX * (nNodeX - 1) + 1
        nY = ndivY * (nNodeY - 1) + 1
        dX = lX / ndivX
        dY = lY / ndivY
        ddX = dX / (nNodeX - 1)
        ddY = dY / (nNodeY - 1)
        numCell = ndivX * ndivY
        numPoin = nX * nY
        numNode = nNodeX * nNodeY
    elif nDime == 3:
        lX, lY, lZ = size
        ndivX, ndivY, ndivZ = shape
        nNodeX, nNodeY, nNodeZ = eshape
        nX = ndivX * (nNodeX - 1) + 1
        nY = ndivY * (nNodeY - 1) + 1
        nZ = ndivZ * (nNodeZ - 1) + 1
        dX = lX / ndivX
        dY = lY / ndivY
        dZ = lZ / ndivZ
        ddX = dX / (nNodeX - 1)
        ddY = dY / (nNodeY - 1)
        ddZ = dZ / (nNodeZ - 1)
        numCell = ndivY * ndivX * ndivZ
        numPoin = nX * nY * nZ
        numNode = nNodeX * nNodeY * nNodeZ

    # set up nodal coordinates
    coords = np.zeros((numPoin, nDime))
    topo = np.zeros((numCell, numNode), dtype=np.int64)
    elem = -1
    if nDime == 1:
        for i in prange(1, ndivX+1):
            elem = i - 1
            for j in prange(1, nNodeX+1):
                n = (nNodeX - 1) * (i - 1) + j
                ne = j - 1
                coords[n - 1, 0] = origo[0] + dX * (i - 1) + ddX * (j - 1)
                topo[elem, ne] = n
    elif nDime == 2:
        for i in prange(1, ndivX + 1):
            for j in prange(1, ndivY + 1):
                elem = (i - 1) * ndivY + j - 1
                for k in prange(1, nNodeX + 1):
                    for m in prange(1, nNodeY + 1):
                        n = ((nNodeX - 1) * (i - 1) + k - 1) * nY + \
                            (nNodeY - 1) * (j - 1) + m
                        ne = (k - 1) * nNodeY + m - 1
                        coords[n - 1, 0] = origo[0] + dX * (i - 1) + \
                            ddX * (k - 1)
                        coords[n - 1, 1] = origo[1] + dY * (j - 1) + \
                            ddY * (m - 1)
                        topo[elem, ne] = n
    elif nDime == 3:
        for i in prange(1, ndivX+1):
            for j in prange(1, ndivY+1):
                for k in prange(1, ndivZ+1):
                    elem = (i - 1) * ndivY * ndivZ + (j - 1) * ndivZ + k - 1
                    for m in prange(1, nNodeX+1):
                        for q in prange(1, nNodeY+1):
                            for p in prange(1, nNodeZ+1):
                                n = (((nNodeX - 1) * (i - 1) + m - 1) * nY +
                                     (nNodeY - 1) * (j - 1) + q - 1) * nZ + \
                                    (nNodeZ - 1) * (k - 1) + p
                                ne = (m - 1) * nNodeY * nNodeZ + \
                                    (q - 1) * nNodeZ + p - 1
                                coords[n - 1, 0] = origo[0] + dX * (i - 1) + \
                                    ddX * (m - 1)
                                coords[n - 1, 1] = origo[1] + dY * (j - 1) + \
                                    ddY * (q - 1)
                                coords[n - 1, 2] = origo[2] + dZ * (k - 1) + \
                                    ddZ * (p - 1)
                                topo[elem, ne] = n
    start -= 1
    return coords, topo + start


@njit(nogil=True, parallel=True, cache=__cache)
def rgrid_2d_bins(xbins, ybins, eshape, origo, start=0):
    # !FIXME
    # size
    lX = xbins.max() - xbins.min()
    lY = ybins.max() - ybins.min()

    # shape of cells
    nEX = len(xbins) - 1
    nEY = len(ybins) - 1

    # number of cells
    nC = nEX * nEY

    # number of nodes
    nNEX, nNEY = eshape
    nNE = nNEX * nNEY
    nNX = nEX * (nNEX - 1) + 1
    nNY = nEY * (nNEY - 1) + 1
    nN = nNX * nNY
    dX = lX / nEX
    dY = lY / nEY
    ddX = dX / (nNEX - 1)
    ddY = dY / (nNEY - 1)

    # create grid
    coords = np.zeros((nN, 3))
    topo = np.zeros((nC, nNE), dtype=np.int64)
    for i in prange(nEX):
        for j in prange(nEY):
            iE = i * nEY + j
            for p in prange(nNEX):
                for q in prange(nNEY):
                    n = (((nNEX - 1) * i + p) * nNY +
                         (nNEY - 1) * j + q) * nNZ + \
                        (nNEZ - 1) * k + r
                    coords[n, 0] = origo[0] + xbins[i] + ddX * p
                    coords[n, 1] = origo[1] + ybins[j] + ddY * q
                    coords[n, 2] = origo[2] + zbins[k] + ddZ * r
                    iNE = p * nNEZ * nNEY + q * nNEZ + r
                    topo[iE, iNE] = n
    return coords, topo + start


@njit(nogil=True, parallel=True, cache=__cache)
def grid_3d_bins(xbins, ybins, zbins, eshape, origo, start=0):

    # size
    lX = xbins.max() - xbins.min()
    lY = ybins.max() - ybins.min()
    lZ = zbins.max() - zbins.min()

    # shape of cells
    nEX = len(xbins) - 1
    nEY = len(ybins) - 1
    nEZ = len(zbins) - 1

    # number of cells
    nC = nEX * nEY * nEZ

    # number of nodes
    nNEX, nNEY, nNEZ = eshape
    nNE = nNEX * nNEY * nNEZ
    nNX = nEX * (nNEX - 1) + 1
    nNY = nEY * (nNEY - 1) + 1
    nNZ = nEZ * (nNEZ - 1) + 1
    nN = nNX * nNY * nNZ
    dX = lX / nEX
    dY = lY / nEY
    dZ = lZ / nEZ
    ddX = dX / (nNEX - 1)
    ddY = dY / (nNEY - 1)
    ddZ = dZ / (nNEZ - 1)

    # create grid
    coords = np.zeros((nN, 3), dtype=xbins.dtype)
    topo = np.zeros((nC, nNE), dtype=np.int64)
    for i in prange(nEX):
        for j in prange(nEY):
            for k in prange(nEZ):
                iE = i * nEZ * nEY + j * nEZ + k
                for p in prange(nNEX):
                    for q in prange(nNEY):
                        for r in prange(nNEZ):
                            n = (((nNEX - 1) * i + p) * nNY +
                                 (nNEY - 1) * j + q) * nNZ + \
                                (nNEZ - 1) * k + r
                            coords[n, 0] = origo[0] + xbins[i] + ddX * p
                            coords[n, 1] = origo[1] + ybins[j] + ddY * q
                            coords[n, 2] = origo[2] + zbins[k] + ddZ * r
                            iNE = p * nNEZ * nNEY + q * nNEZ + r
                            topo[iE, iNE] = n
    return coords, topo + start


if __name__ == '__main__':

    size = Lx, Ly, Lz = 800, 600, 20
    shape = nx, ny, nz = 8, 6, 2
    eshape = 3, 3, 3
    origo = 0, 0, 0
    start = 0

    coordsQ9, topoQ9 = grid(size=size, shape=shape, eshape=eshape)
    coordsQ9_ST, topoQ9_ST = rgridST(size=size, shape=shape, eshape=eshape,
                                     origo=origo, start=start)
    coordsQ9_MT, topoQ9_MT = rgridMT(size=size, shape=shape, eshape=eshape,
                                     origo=origo, start=start)

    xbins = np.linspace(0, Lx, nx+1)
    ybins = np.linspace(0, Ly, ny+1)
    zbins = np.linspace(0, Lz, nz+1)
    coords, topo = grid_3d_bins(xbins, ybins, zbins, eshape, origo)

    print(len(xbins))

    pass

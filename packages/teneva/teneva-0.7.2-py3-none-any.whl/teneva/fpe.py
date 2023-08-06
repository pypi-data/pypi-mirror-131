import math
import numpy as np
from scipy.linalg import expm
from scipy.linalg import toeplitz
import time
from time import perf_counter as tpc
from tqdm import tqdm


from .grid import ind2poi_cheb


from .tensor import accuracy
from .tensor import copy
from .cross import cross
from .tensor import erank
from .tensor import norm
from .tensor import rand
from .tensor import truncate


def odes(f, y0, t, n, h):
    y = y0.copy()
    for _ in range(1, n):
        k1 = h * f(y, t)
        k2 = h * f(y + 0.5 * k1, t + 0.5 * h)
        k3 = h * f(y + 0.5 * k2, t + 0.5 * h)
        k4 = h * f(y + k3, t + h)
        y+= (k1 + 2 * (k2 + k3) + k4) / 6.
        t+= h
    return y


def cheb_ind(d, n):
    I = []
    for k in range(d):
        I.append(np.arange(n).reshape(1, -1))
    I = np.meshgrid(*I, indexing='ij')
    I = np.array(I).reshape((d, -1), order='F')
    return I





def cheb_pol(X, m, l):
    X = (2. * X - l[1] - l[0]) / (l[1] - l[0])
    T = np.ones([m] + list(X.shape))
    if m < 2: return T
    T[1, ] = X.copy()
    for k in range(2, m):
        T[k, ] = 2. * X * T[k - 1, ] - T[k - 2, ]
    return T


def cheb_bld(f, d, n, l, e=1.E-6, Z=None, verb=False):
    Z = rand([n]*d, 1) if Z is None else Z
    Y = cross(lambda I: f(ind2poi_cheb(I.T.astype(int), l[0], l[1], n)),
              Z, nswp=3, kr=1, rf=1) # eps=e
    Y = truncate(Y, e)
    return Y


def cheb_int(G, e=1.E-6):
    G = copy(G)
    for k in range(len(G)):
        r, m, q = G[k].shape
        G[k] = np.swapaxes(G[k], 0, 1)
        G[k] = G[k].reshape((m, -1))
        G[k] = np.vstack([G[k], G[k][m-2 : 0 : -1, :]])
        G[k] = np.fft.fft(G[k], axis=0).real
        G[k] = G[k][:m, :] / (m - 1)
        G[k][0, :] /= 2.
        G[k][m-1, :] /= 2.
        G[k] = G[k].reshape((m, r, q))
        G[k] = np.swapaxes(G[k], 0, 1)
    G = truncate(G, e)
    return G


def cheb_get(X, A, l, z=0.):
    G = A
    d = len(G)
    n = G[0].shape[1]
    T = cheb_pol(X, n, l)
    Y = np.ones(X.shape[1]) * z
    l1 = np.ones(d) * l[0]
    l2 = np.ones(d) * l[1]
    for j in range(X.shape[1]):
        if np.max(l1-X[:, j]) > 1.E-16 or np.max(X[:, j]-l2) > 1.E-16: continue
        Q = np.einsum('riq,i->rq', G[0], T[:, 0, j])
        for i in range(1, d):
            Q = Q @ np.einsum('riq,i->rq', G[i], T[:, i, j])
        Y[j] = Q[0, 0]
    return Y


def cheb_gets(A, l, m=None, e=1.E-6):
    G = A
    d = len(G)
    n = G[0].shape[1]
    m = m or n
    I = np.arange(m).reshape((1, -1))
    X = ind2poi_cheb(I, l[0], l[1], m).reshape(-1)
    T = cheb_pol(X, n, l)
    Q = []
    for i in range(d):
        Q.append(np.einsum('riq,ij->rjq', G[i], T))
    Q = truncate(Q, e)
    return Q


def cheb_sum(A, l):
    G = A
    d = len(G)
    v = np.array([[1.]])
    for k in range(d):
        r, m, q = G[k].shape
        G[k] = np.swapaxes(G[k], 0, 1)
        G[k] = G[k].reshape(m, -1)
        p = np.arange(G[k].shape[0])[::2]
        p = np.repeat(p.reshape(-1, 1), G[k].shape[1], axis=1)
        G[k] = np.sum(G[k][::2, :] * 2. / (1. - p**2), axis=0)
        G[k] = G[k].reshape(r, q)
        v = v @ G[k]
        v*= (l[1] - l[0]) / 2.
    return v[0, 0]


def difs(m, n, l):
    l_min, l_max = l

    n1 = np.int(np.floor(n / 2))
    n2 = np.int(np.ceil(n / 2))
    k = np.arange(n)
    th = k * np.pi / (n - 1)

    T = np.tile(th/2, (n, 1))
    DX = 2. * np.sin(T.T + T) * np.sin(T.T - T)
    DX[n1:, :] = -np.flipud(np.fliplr(DX[0:n2, :]))
    DX[range(n), range(n)] = 1.
    DX = DX.T

    Z = 1. / DX
    Z[range(n), range(n)] = 0.

    C = toeplitz((-1.)**k)
    C[+0, :]*= 2
    C[-1, :]*= 2
    C[:, +0]*= 0.5
    C[:, -1]*= 0.5

    D_list = []
    D = np.eye(n)
    l = 2. / (l_max - l_min)
    for i in range(m):
        D = (i + 1) * Z * (C * np.tile(np.diag(D), (n, 1)).T - D)
        D[range(n), range(n)] = -np.sum(D, axis=1)
        D_list.append(D * l)
        l = l * l

    return D_list


def prep_diff(n, l, h, Dc):
    D1, D2 = difs(2, n, l)
    h0 = h / 2
    J0 = np.eye(n)
    J0[+0, +0] = 0.
    J0[-1, -1] = 0.
    Z0 = expm(h0 * Dc * J0 @ D2)
    return Z0


def calc_diff(G, Z0, e=1.E-6):
    d = len(G)
    for k in range(d):
        G[k] = np.einsum('ij,kjm->kim', Z0, G[k])
    G = truncate(G, e)
    return G


def calc_conv(t, A, Y0, f0, f1, d, n, l, h, e=1.E-6):
    def func(y, t):
        X, r = y[:-1, :], y[-1, :]
        return np.vstack([f0(X, t), -np.sum(f1(X, t), axis=0) * r])
    def step(X):
        X0 = odes(f0, X, t, 2, -h)
        w0 = cheb_get(X0, A, l)
        y0 = np.vstack([X0, w0])
        y1 = odes(func, y0, t-h, 2, h)
        w1 = y1[-1, :]
        return w1
    return cheb_bld(step, d, n, l, e, Y0)


def fpe(d, n, l, m, h, Dc, f0, f1, r0, rt=None, rs=None, e=None, cb_=None, with_hist=True):
    res = { 'e_rank': [], 'e_real': [], 'e_stat': [], 't_calc': 0., 's': [] }
    tqdm_ = tqdm(desc='Solve', unit='step', total=m-1, ncols=90)

    Ys = cheb_bld(rs, d, n, l, (e or 1.E-6)/100) if rs else None

    t_ = time.perf_counter()

    Z = prep_diff(n, l, h, Dc)
    Y = cheb_bld(r0, d, n, l, e)
    W = copy(Y)
    t = 0

    res['t_calc']+= time.perf_counter() - t_

    for m_ in range(1, m+1):
        t_ = time.perf_counter()

        t+= h
        Y = calc_diff(Y, Z, e)
        A = cheb_int(Y, e)
        Y = calc_conv(t, A, W, f0, f1, d, n, l, h, e)
        A = cheb_int(Y, e)
        s = 1. / cheb_sum(A, l)
        Y[0] *= s
        W = copy(Y)
        Y = calc_diff(Y, Z, e)

        res['t_calc']+= time.perf_counter() - t_
        res['e_rank'].append(erank(Y))
        res['s'].append(s)

        if cb_ is not None: # Callback
            cb_(Y, res)

        msg = f'|t={t:-4.2f}|'
        msg+= f'r={erank(Y):-3.1f}|'
        if with_hist or m_ == m:
            if rt:
                Yt = cheb_bld(lambda X: rt(X, t), d, n, l, (e or 1.E-6)/100)
                e_ = accuracy(Y, Yt)
                res['e_real'].append(e_)
                msg+= f'e_r={e_:-8.2e}|'
            if Ys is not None:
                e_ = accuracy(Y, Ys)
                res['e_stat'].append(e_)
                msg+= f'e_s={e_:-8.2e}|'

        tqdm_.set_postfix_str(msg, refresh=True)
        tqdm_.update(1)

    tqdm_.close()
    if with_hist:
        print(f'\nComputation time {res["t_calc"]:-8.2f} sec')
    return res

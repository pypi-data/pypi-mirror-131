import numpy as np


def core_one(n, r):
    return np.kron(np.ones([1, n, 1]), np.eye(r)[:, None, :])


def core_orthogonalize(Z, k):
    # Z = [G.copy() for G in Y]
    L = np.array([[1.]])
    R = np.array([[1.]])
    for i in range(0, k):
        G = _reshape(Z[i], [-1, Z[i].shape[2]])
        Q, R = np.linalg.qr(G, mode='reduced')
        Z[i] = _reshape(Q, Z[i].shape[:-1] + (Q.shape[1], ))
        G = _reshape(Z[i+1], [Z[i+1].shape[0], -1])
        Z[i+1] = _reshape(np.dot(R, G), (R.shape[0], ) + Z[i+1].shape[1:])
    for i in range(len(Z)-1, k, -1):
        G = _reshape(Z[i], [Z[i].shape[0], -1])
        L, Q = scipy.linalg.rq(G, mode='economic', check_finite=False)
        Z[i] = _reshape(Q, (Q.shape[0], ) + Z[i].shape[1:])
        G = _reshape(Z[i-1], [-1, Z[i-1].shape[2]])
        Z[i-1] = _reshape(np.dot(G, L), Z[i-1].shape[:-1] + (L.shape[1], ))
    return Z


def _reshape(a, shape):
    return np.reshape(a, shape, order='F')

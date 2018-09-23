import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans

class KEstimator:

    def __init__(self):
        self.K = 0

    def calculate_s_k(self, X, k):
        km = MiniBatchKMeans(n_clusters=k, random_state=42).fit(X)
        return km.inertia_  # -km.score(df) #

    @staticmethod
    def alpha_k(k, a_k, dim):
        if k == 2:
            ak = 1.0 - 3.0 / (4.0 * dim)
        else:
            ak1 = a_k[k - 1]
            ak = ak1 + (1.0 - ak1) / 6.0
        a_k[k] = ak
        return ak

    def cluster_eval(self, s_k, a_k, k, dim):
        if k == 1:
            return 1.0
        elif k == 2:
            a_k[1] = 0.0

        a_k[k] = self.alpha_k(k, a_k, dim)
        if a_k[k - 1] != 0.0:
            return s_k[k] / (a_k[k - 1] * s_k[k - 1])
        else:
            return 1.0

    def fit(self, X, max_k=50):
        s_k = dict()
        a_k = dict()
        f_k = np.ones(max_k)

        if isinstance(X, pd.DataFrame):
            dim = len(X.columns)
        elif isinstance(X, np.ndarray):
            dim = X.shape[1]

        for k in range(1, max_k + 1):
            i = k - 1
            s_k[k] = self.calculate_s_k(X, k)
            f_k[i] = self.cluster_eval(s_k, a_k, k, dim)
        self.K = np.argmin(f_k) + 1
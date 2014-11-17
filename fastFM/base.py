import numpy as np
import ffm
import scipy.sparse as sp
from scipy.stats import norm
from sklearn.utils import assert_all_finite
from sklearn.base import BaseEstimator, ClassifierMixin

def _validate_class_labels(y):
        assert len(set(y)) == 2
        assert y.min() == -1
        assert y.max() == 1

class FactorizationMachine(BaseEstimator):

    def __init__(self, max_iter=100, init_var=0.1, rank=8, random_state=123):
        self.max_iter = max_iter
        self.random_state = random_state
        self.init_var = init_var
        self.rank = rank
        self.l2_reg_w = 0
        self.l2_reg_V = 0
        self.step_size = 0

    def predict(self, X_test):
        """ Return predictions

        Parameters
        ----------
        X : scipy.sparse.csc_matrix, (n_samples, n_features)

        Returns
        ------

        T : array, shape (n_samples)
            The labels are returned for classification.

        """
        assert_all_finite(X_test)
        assert sp.isspmatrix_csc(X_test)
        assert X_test.shape[1] == len(self.w_)
        return ffm.ffm_predict(self.w0_, self.w_, self.V_, X_test)


class BaseFMClassifier(FactorizationMachine, ClassifierMixin):


    def predict(self, X_test):
        pred = super(BaseFMClassifier, self).predict(X_test)
        pred = norm.cdf(pred)
        # convert probs to labels
        pred[pred < 0.5] = -1
        pred[pred >= 0.5] = 1
        print "predict"
        return pred


    def predict_proba(self, X_test):
        """ Return probabilities

        Parameters
        ----------
        X : scipy.sparse.csc_matrix, (n_samples, n_features)

        Returns
        ------

        T : array, shape (n_samples)
            Class Probabilities

        """
        pred = super().predict(self, X_test)
        return norm.cdf(pred)

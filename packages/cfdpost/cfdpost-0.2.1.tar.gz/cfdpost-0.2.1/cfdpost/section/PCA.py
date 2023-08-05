'''
Extract flow features of airfoils or wing sections.

https://scikit-learn.org/stable/modules/classes.html#module-sklearn.decomposition

'''
import pickle
import copy

import numpy as np
from sklearn.decomposition import PCA, KernelPCA


class PCASec():
    '''
    Extract features of airfoil wall Mach number distribution

    >>> pca = PCASec(n_point: int, n_feature=None, whiten=False, svd_solver='auto')

    PCA: principal component analysis

    https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

    ### Input:
    ```text
        n_point:        data size of an airfoil
        n_feature:      intensional size of features (or None, or 'mle')
        whiten:         whitening of the PCA
        svd_solver:     'auto', 'full', 'arpack', 'randomized'
    ```

    ### Attributes:
    ```text
        _low, _upp:     lower and upper bound of the data
        n_sample:       number of training samples
        x_train:        unscaled training samples, ndarray [n_sample, n_point]
        model:          estimator
    ```

    '''

    def __init__(self, n_point: int, n_feature=None, whiten=False, svd_solver='auto'):

        self.n_point = n_point
        self.n_feature = n_feature

        self._low = 0.0
        self._upp = 1.0

        self.model = PCA(n_components=n_feature, copy=True, whiten=whiten, svd_solver=svd_solver)

    def train(self, x_data):
        '''
        Fit the model with x_data

        ### Inputs:
        ```text
        x_data:     ndarray [n_sample, n_point]
        ```
        '''
        if not isinstance(x_data, np.ndarray):
            raise Exception('Must provide ndarray')
        elif x_data.shape[1] != self.n_point:
            raise Exception('Must provide ndarray, shape [n_sample, n_point]')
        
        self.n_sample = x_data.shape[0]
        self.x_train = x_data.copy()
        xx = (self.x_train-self._low)/(self._upp-self._low)

        self.model.fit(xx)

        if not isinstance(self.n_feature, int):
            self.n_feature = self.model.n_components_
    
    def save_rawdata(self, fname='Raw.bin'):
        '''
        Save the raw data of PCA training
        '''
        with open(fname, 'wb') as f:
            pickle.dump(self.n_sample, f)
            pickle.dump(self.n_point, f)

            for i in range(self.n_sample):
                pickle.dump(self.x_train[i,:], f)

    def load_rawdata(self, fname='Raw.bin'):
        '''
        Load the raw data of PCA training
        '''
        with open(fname, 'rb') as f:
            self.n_sample = pickle.load(f)
            self.n_point  = pickle.load(f)

            x_data = np.zeros([self.n_sample, self.n_point])
            for i in range(self.n_sample):
                x = pickle.load(f)
                x_data[i,:] = copy.deepcopy(np.array(x))

            self.train(x_data)

    def transform(self, x_data) -> np.ndarray:
        '''
        Apply dimensionality reduction to x_data

        ### Inputs:
        ```text
        x_data:     ndarray [n, n_point]
        ```
        ### Return:
        ```text
        data_:      ndarray [n, n_feature]
        ```
        '''
        if not isinstance(x_data, np.ndarray):
            raise Exception('Must provide ndarray')
        elif x_data.shape[1] != self.n_point:
            raise Exception('Must provide ndarray, shape [n, n_point]')

        data_ = (x_data-self._low)/(self._upp-self._low)

        return self.model.transform(data_)

    def inverse_transform(self, data_) -> np.ndarray:
        '''
        Transform data back to its original space

        ### Inputs:
        ```text
        data_:      ndarray [n, n_feature]
        ```
        ### Return:
        ```text
        x_data:     ndarray [n, n_point]
        ```
        '''
        if not isinstance(data_, np.ndarray):
            raise Exception('Must provide ndarray')
        elif data_.shape[1] != self.n_feature:
            raise Exception('Must provide ndarray, shape [n, n_feature]')

        x_data = self.model.inverse_transform(data_)
        x_data = x_data*(self._upp-self._low) + self._low
    
        return x_data

    def standard_x_distribution(self):
        '''
        Desired X distribution: xx (ndarray [n_point])

        From lower surface trailing edge to upper surface trailing edge
        '''
        n = int((self.n_point+1)/2)
        x0 = np.zeros(n)
        for i in range(n):
            x0[i] = clustcos(i, n)
        x1 = np.flip(x0, axis=0)
        xx = np.concatenate((x1, x0[1:]), axis=0)

        return xx

    @property
    def explained_variance(self):
        '''
        The amount of variance explained by each of the selected components.

        Equal to n_feature largest eigenvalues of the covariance matrix of X.

        ### Return:
        ```text
        variance:   ndarray [n_feature]
        ```
        '''
        return self.model.explained_variance_

    @property
    def explained_variance_ratio(self):
        '''
        Percentage of variance explained by each of the selected components.

        If n_feature is not set then all components are stored and the sum of the ratios is equal to 1.0.

        ### Return:
        ```text
        variance:   ndarray [n_feature]
        ```
        '''
        return self.model.explained_variance_ratio_

    @property
    def total_component_energy(self) -> float:
        '''
        The total energy represented by the n_feature PCA components
        ''' 
        return np.sum(self.model.explained_variance_ratio_)


class KPCASec(PCASec):
    '''
    Extract features of airfoil wall Mach number distribution

    KPCA: kernel principal component analysis

    https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.KernelPCA.html

    ### Input:
    ```text
        n_point:        data size of an airfoil
        n_feature:      intensional size of features (or None)
        kernel:         'linear', 'poly', 'rbf', 'sigmoid', 'cosine', 'precomputed'
        eigen_solver:   'auto', 'dense', 'arpack'   
        n_jobs:         number of parallel jobs to run (-1 means using all processors)
    ```

    ### Attributes:
    ```text
        _low, _upp:     lower and upper bound of the data
        n_sample:       number of training samples
        x_train:        unscaled training samples, ndarray [n_sample, n_point]
        model:          estimator
    ```

    '''

    def __init__(self, n_point: int, n_feature=None, kernel='linear', eigen_solver='auto', n_jobs=1):
        super().__init__(n_point, n_feature)

        self.model = KernelPCA(n_components=n_feature, kernel=kernel, eigen_solver=eigen_solver, copy_X=True, n_jobs=n_jobs)

        self.model.fit_inverse_transform = True

    @property
    def explained_variance(self):
        '''
        The amount of variance explained by each of the selected components.

        Equal to n_feature largest eigenvalues of the covariance matrix of X.

        ### Return:
        ```text
        variance:   ndarray [n_feature]
        ```
        '''
        return self.model.lambdas_

    @property
    def explained_variance_ratio(self):
        '''
        Not defined
        ```
        '''
        return self.model.lambdas_

    @property
    def total_component_energy(self) -> float:
        '''
        Not defined
        ''' 
        return 1.0


#* The same as cst-modeling3d
#* https://github.com/swayli94/cst-modeling3d

def clustcos(i: int, nn: int, a0=0.0079, a1=0.96, beta=1.0) -> float:
    '''
    Point distribution on x-axis [0, 1]. (More points at both ends)

    >>> c = clustcos(i, n, a0, a1, beta)

    ### Inputs:
    ```text
    i:      index of current point (start from 0)
    nn:     total amount of points
    a0:     parameter for distributing points near x=0
    a1:     parameter for distributing points near x=1
    beta:   parameter for distribution points 
    ```
    '''
    aa = np.power((1-np.cos(a0*np.pi))/2.0, beta)
    dd = np.power((1-np.cos(a1*np.pi))/2.0, beta) - aa
    yt = i/(nn-1.0)
    a  = np.pi*(a0*(1-yt)+a1*yt)
    c  = (np.power((1-np.cos(a))/2.0,beta)-aa)/dd

    return c

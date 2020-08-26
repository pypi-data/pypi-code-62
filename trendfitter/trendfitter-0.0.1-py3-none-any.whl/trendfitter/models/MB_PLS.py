from numpy import array, isnan, nansum, nan_to_num, multiply, sum, sqrt, \
                  append, zeros, place, nan, concatenate, mean, nanvar,  \
                  std, unique, where, nanmean
from numpy.linalg import norm, pinv
from sklearn.model_selection import KFold
from pandas import DataFrame, Series
from trendfitter.auxiliary.tf_aux import scores_with_missing_values
from . import PLS

class MB_PLS:
    """
    A sklearn-like class for the Multi-Block Projection to Latent Structures.

        Parameters
        ----------
        cv_splits_number : int, optional
            number of splits used for cross validation in case latent_variables is None
        tol : float, optional
            value used to decide if model has converged
        loop_limit : int, optional
            maximum number of loops for the extraction of one latent variable
        missing_values_method : str, optional
            string to define the method that the model will deal with missing values

        Attributes
        ----------
        latent_variables : int
            list of number of latent variables deemed relevant from each block. 
        block_divs : [int]
            list with the index of every block final position. ex. [2,4] means two blocks with 
                columns 0 and 1 on the first block and columns 2 and 3 on the second block. 
                Assigned when fit method runs.
        p_loadings_block : [array_like]
            list of p loadings arrays of every block with all the extracted latent variables 
        superlevel_p_loadings : array_like
            array of all latent variables extracted p loadings for the super level
        weights_block : [array_like]
            list of weights arrays of every block with all the extracted latent variables 
        weights_super : array_like
            array of all latent variables extracted weights for the super level
        c_loadings : array_like
            array of c_loadings for all extracted latent variables
        q2 : [float]
            list of r² coefficients extracted during cross validation
        feature_importances : [float]
            list of values that represent how important is each variable in the same order 
                of the X columns on the first matrix

        Methods
        -------
        fit(X, blocks_sep, Y)
            Applies the NIPALS like method to find the best parameters that adjust the model 
                to the data
        transform(X)
            Transforms the original data to the latent variable space in the super level 
        transform_inv(scores)
            Returns the superlevel scores to the original data space
        transform_b(X, block)
            Transforms the original data to the latent variable space in the block level for
                all blocks
        predict(X)
            Predicts Y values 
        score(X, Y)
            calculates the r² value for Y
        Hotellings_T2(X)
            Calculates Hotellings_T2 values for the X data in the super level
        Hotellings_T2_blocks(X)
            Calculates Hotellings_T2 values for in the block level for all blocks
        SPEs_X(X)
            Calculates squared prediction errors on the X side for the super level
        SPEs_X_blocks(X)
            Calculates squared prediction errors for the block level for all blocks
        SPEs_Y(X, Y)
            Calculates squared prediction errors for the predictions
        contributions_scores(X)
            calculates the contributions of each variable to the scores on the super level
        contributions_scores_b(X)
            calculates the contributions of each variable to the scores on the super level
        contributions_SPE(X)
            calculates the contributions of each variable to the SPE on the X side for
                the super level
        contributions_SPE_b(X)
            calculates the contributions of each variable to the SPE on the X side for
                the block level for all blocks

    """
    def __init__(self, cv_splits_number = 7, tol = 1e-16, loop_limit = 1000, missing_values_method = 'TSM'):
        
        # Parameters
        
        self.cv_splits_number = cv_splits_number # number of splits for latent variable cross-validation
        self.tol = tol # criteria for convergence
        self.loop_limit = loop_limit # maximum number of loops before convergence is decided to be not attainable
        self.q2y = [] # list of cross validation scores
        self.missing_values_method = missing_values_method
        
        # Attributes

        self.latent_variables = None # number of principal components to be extracted
        self.block_divs = None
        self.block_p_loadings = None
        self.superlevel_p_loadings = None
        self.block_weights = None
        self.superlevel_weights = None
        self.x_weights_star = None
        self.x_weights = None
        self.c_loadings = None 
        self.feature_importances_ = None
        self.coefficients = None
        self.omega = None # score covariance matrix for missing value estimation
        self._int_PLS = None

    def fit(self, X, block_divs, Y, latent_variables = None, deflation = 'both', int_call = False):
        """
        Adjusts the model parameters to best fit the Y using the algorithm defined in 
            Westerhuis et al's [1]

        Parameters
        ----------
        X : array_like
            Matrix with all the data to be used as predictors in one only object
        block_divs : [int]
            list with the index of every block final position. ex. [2,4] means two blocks with 
                columns 0 and 1 on the first block and columns 2 and 3 on the second block.
        Y : array_like
            Matrix with all the data to be predicted in one only object
        latent_variables : int, optional
            Number of latent variables deemed relevant from each block. If left unspecified
                a cross validation routine will define the number during fitting
        deflation : str, optional
            string defining method of deflation, only Y or both X and Y 
        int_call : Boolean, optional
            Flag to define if it is an internal call on the cross validation routine and decide
                if it is necessary to calculate the VIP values

        References 
        ----------
        [1] J. A. Westerhuis, T. Kourti, and J. F. MacGregor, “Analysis of multiblock and hierarchical 
        PCA and PLS models,” Journal of Chemometrics, vol. 12, no. 5, pp. 301–321, 1998, 
        doi: 10.1002/(SICI)1099-128X(199809/10)12:5<301::AID-CEM515>3.0.CO;2-S.


        """
        if isinstance(X, DataFrame):# If X data is a pandas Dataframe
            indexes = X.index.copy()
            X_columns = X.columns.copy()
            X = array(X.to_numpy(), ndmin = 2)

        missing_values_list = [isnan(sum(X[:, start:end])) for (start, end) in block_coord_pairs] 
          
        if isinstance( Y, DataFrame ) or isinstance( Y, Series ): # If Y data is a pandas Dataframe or Series 
            if isinstance( Y, DataFrame ) : Y_columns = Y.columns
            Y = array( Y.to_numpy(), ndmin = 2 ).T
            
        Orig_X = X
        Orig_Y = Y
        
        #Using a full PLS as basis to calculate the MB-PLS
        int_PLS = PLS(cv_splits_number = self.cv_splits_number, tol = self.tol, loop_limit = self.loop_limit, missing_values_method = self.missing_values_method)
        int_PLS.fit(X, Y, latent_variables = latent_variables, deflation = deflation)

        

        block_coord_pairs = (*zip([0] + block_divs[:-1], block_divs),)

        superlevel_T = zeros((X.shape[0], len(block_coord_pairs) * int_PLS.latent_variables))
        block_weights = zeros((int_PLS.latent_variables * len(block_coord_pairs), X.shape[1]))

        for block, (start, end) in enumerate(block_coord_pairs):
            test_missing_data = isnan(sum(X[:, start:end]))
            if test_missing_data:
                b_weights = zeros((int_PLS.latent_variables, end - start))
                for i in range(int_PCA.latent_variables):
                    b_weights[i, :] = nansum(X[:, start:end] * array(int_PLS.training_scores[:, i], ndmin = 2).T, axis = 0) / nansum(((~isnan(X[:, start:end]).T * int_PLS.training_scores[:, i]) ** 2), axis = 1)
            else:
                b_weights = array(X[:, start:end].T @ int_PLS.training_scores / diagonal(int_PLS.training_scores.T @ int_PLS.training_scores), ndmin = 2).T

            block_weights[(block * int_PLS.latent_variables):((block + 1) * int_PLS.latent_variables), start:end] = b_weights
            
            block_scores = zeros((X.shape[0], int_PCA.principal_components))
            if test_missing_data:
                for i in range(int_PCA.principal_components):
                    block_scores[:, i] = nansum(X[:, start:end] * block_weights[i, :], axis = 1) / nansum(((~isnan(X[:, start:end]) * block_weights[i, :]) ** 2), axis = 1)
            else:
                block_scores = (X[:, start:end] @ b_loadings.T) 

            superlevel_T[:, [block + num * len(block_coord_pairs) for num, _ in enumerate(block_coord_pairs)]] = block_scores
        
        superlevel_weights = (superlevel_T.T @ int_PLS.scores) / (int_PLS.scores.T @ int_PLS.scores)

        #----------------Attribute Assignment---------------

        self.latent_variables = int_PLS.latent_variables
        self.block_divs = block_divs
        self.block_p_loadings = None


        self.block_weights = block_weights
        self.superlevel_weights = superlevel_weights
        self.x_weights_star = int_PLS.weights_star
        self.x_weights = int_PLS.weights
        self.c_loadings = int_PLS.c_loadings
        self.feature_importances_ = int_PLS.feature_importances_
        self.omega = int_PLS.omega
        self._int_PLS = int_PLS

    
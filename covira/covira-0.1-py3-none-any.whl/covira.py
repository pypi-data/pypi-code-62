import numpy as np

class Covira:
    '''
    CoVIRA (Consensus by Voting with Iterative Re-weighting based on Agreement) is a method
    to identify weights and produce consensus predictions based on a collection of results from
    predictors for multiple samples. It employs a iterative recalculations of weights based on the
    weighted "agreement" between the predictors, and allows the calculation of a final prediction as well.

    This algorithm was created to help on the integration of results from multiple prediction tools in a
    reverse vaccinology study where no validation dataset was available for all features been inferred. Therefore,
    we created a unsupervised way to estimate how accurate each predictor was for that particular case considering
    that the more the results of a predictor is "consfirmed" by the others, the higher it's accuracy.

    Reference:

        Grassmann AA, Kremer FS, Dos Santos JC, Souza JD, Pinto LDS, McBride AJA. Discovery of Novel Leptospirosis Vaccine 
        Candidates Using Reverse and Structural Vaccinology. Front Immunol. 2017;8:463. Published 2017 Apr 27. 
        doi:10.3389/fimmu.2017.00463
    '''

    def __init__(self, max_iterations: int = 10000) -> None:
        '''
        Constructor.

        Args:
            max_iterations: maximum number of iterations during weight recalculation.

        Returns:
            None.
        '''
        self.max_iterations = max_iterations
        self._weights = None

    def fit(self, predictions: np.array) -> None:
        '''
        Receives a n x m numpy array (with 'n' samples classified by 'm' binary predictors), and 
        calculates the weight for each predictor based on their weighted agreement. 
        
        Args:
            predictions: numpy array with predictors calculated for different samples.

        Returns:
            None.
        '''
        self._weights = [1./predictions.shape[1] for i in range(predictions.shape[1])]

        for i in range(self.max_iterations):
            updated_weights = self._update_weights(predictions)

            if list(self.weights) == list(updated_weights):
                break

            else:
                self._weights = updated_weights

    def _update_weights(self, predictions: np.array) -> np.array:
        '''
        Updated the weights of the predictors.
        
        Args:
            predictions: numpy array with predictors calculated for different samples.

        Returns:
            None.
        '''
        accuracies = []

        for w, prediction_weight in enumerate(self._weights):
            accuracy_dividend = 0
            accuracy_divisor = 0

            for sample_i, sample in enumerate(predictions):
                for p, prediction in enumerate(sample):
                    if p != w:
                        if prediction == sample[w]:
                            accuracy_dividend += 1 * prediction_weight
                        accuracy_divisor += 1 * prediction_weight

            accuracies.append(accuracy_dividend/accuracy_divisor)

        return np.array([float(i/sum(accuracies)) for i in accuracies])

    def predict(self, predictions):
        '''
        Returns the consensus prediction.
        
        Args:
            predictions: numpy array with predictors calculated for different samples.

        Returns:
            consensus_predictions (np.array).
        '''
        consensus_predictions = np.sum(predictions * self._weights, axis=1)
        return consensus_predictions

    @property
    def weights(self):
        '''
        Returns the weights calculated for each predictor.
        
        Args:
            None.

        Returns:
            weights (np.array).
        '''
        return self._weights
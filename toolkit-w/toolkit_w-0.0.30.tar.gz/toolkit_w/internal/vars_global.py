import os
from enum import Enum
import pytest

script_dir = os.path.dirname(__file__)


class Pipeline(Enum):
    DATA_CLEANING_POST_IMPUTATION = 'data_cleaning_post_imputation'
    TIME_SERIES_AUTO_FEATURES = 'time_series_auto_features'
    FEATURE_EMBEDDING = 'feature_embedding'
    FEATURE_SELECTION = 'feature_selection'
    DATA_CLEANING_PRE_IMPUTATION = 'data_cleaning_pre_imputation'
    IMPUTATION = 'imputation'
    TEXT_PREPROCESSING = 'text_preprocessing'
    FEATURE_ENGINEERING = 'feature_engineering'
    FEATURE_STACKING = 'feature_stacking'
    ESTIMATOR = 'estimator'
    BALANCING = 'balancing'
    AUTO_SAMPLE_GENERATION = 'auto_sample_generation'

    @staticmethod
    def ALL_CLASSIFICATION():
        return [Pipeline.DATA_CLEANING_PRE_IMPUTATION, Pipeline.TEXT_PREPROCESSING, Pipeline.IMPUTATION,
                Pipeline.DATA_CLEANING_POST_IMPUTATION, Pipeline.AUTO_SAMPLE_GENERATION, Pipeline.BALANCING,
                Pipeline.FEATURE_ENGINEERING, Pipeline.FEATURE_STACKING, Pipeline.FEATURE_EMBEDDING,
                Pipeline.FEATURE_SELECTION, Pipeline.ESTIMATOR]

    @staticmethod
    def ALL_CLASSIFICATION_TIMESERIES():
        return [Pipeline.DATA_CLEANING_PRE_IMPUTATION, Pipeline.TEXT_PREPROCESSING, Pipeline.IMPUTATION,
                Pipeline.DATA_CLEANING_POST_IMPUTATION, Pipeline.BALANCING, Pipeline.FEATURE_ENGINEERING,
                Pipeline.FEATURE_STACKING, Pipeline.FEATURE_EMBEDDING, Pipeline.FEATURE_SELECTION, Pipeline.ESTIMATOR]

    @staticmethod
    def ALL_MULTIVARIATE_TIMESERIES():
        return [Pipeline.DATA_CLEANING_PRE_IMPUTATION, Pipeline.TEXT_PREPROCESSING, Pipeline.IMPUTATION,
                Pipeline.DATA_CLEANING_POST_IMPUTATION, Pipeline.TIME_SERIES_AUTO_FEATURES,
                Pipeline.FEATURE_ENGINEERING, Pipeline.FEATURE_STACKING, Pipeline.FEATURE_EMBEDDING,
                Pipeline.FEATURE_SELECTION, Pipeline.ESTIMATOR]

    @staticmethod
    def ALL_ANOMALY():
        return [Pipeline.DATA_CLEANING_PRE_IMPUTATION, Pipeline.TEXT_PREPROCESSING, Pipeline.IMPUTATION,
                Pipeline.DATA_CLEANING_POST_IMPUTATION, Pipeline.AUTO_SAMPLE_GENERATION, Pipeline.BALANCING,
                Pipeline.FEATURE_ENGINEERING, Pipeline.FEATURE_STACKING, Pipeline.FEATURE_EMBEDDING,
                Pipeline.FEATURE_SELECTION, Pipeline.ESTIMATOR]

    @staticmethod
    def ALL_REGRESSION():
        return [Pipeline.DATA_CLEANING_PRE_IMPUTATION, Pipeline.TEXT_PREPROCESSING, Pipeline.IMPUTATION,
                Pipeline.DATA_CLEANING_POST_IMPUTATION, Pipeline.AUTO_SAMPLE_GENERATION, Pipeline.FEATURE_ENGINEERING,
                Pipeline.FEATURE_STACKING, Pipeline.FEATURE_EMBEDDING, Pipeline.FEATURE_SELECTION, Pipeline.ESTIMATOR]

    @staticmethod
    def ALL_REGRESSION_TIMESERIES():
        return [Pipeline.DATA_CLEANING_PRE_IMPUTATION, Pipeline.TEXT_PREPROCESSING, Pipeline.IMPUTATION,
                Pipeline.DATA_CLEANING_POST_IMPUTATION, Pipeline.TIME_SERIES_AUTO_FEATURES,
                Pipeline.FEATURE_ENGINEERING, Pipeline.FEATURE_STACKING, Pipeline.FEATURE_EMBEDDING,
                Pipeline.FEATURE_SELECTION, Pipeline.ESTIMATOR]


class ProblemType(Enum):
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'
    ANOMALY_DETECTION = 'anomaly_detection'
    TIMESERIES_CLASSIFICATION = 'classification_timeseries'
    TIMESERIES_REGRESSION = 'regression_timeseries'
    TIMESERIES_ANOMALY_DETECTION = 'anomaly_timeseries'

# class ProblemType(Enum):
#     CLASSIFICATION = 'firefly.enums.ProblemType.CLASSIFICATION'
#     REGRESSION = 'firefly.enums.ProblemType.REGRESSION'
#     ANOMALY_DETECTION = 'firefly.enums.ProblemType.ANOMALY_DETECTION'
#     # @param['firefly.enums.ProblemType.REGRESSION', 'firefly.enums.ProblemType.CLASSIFICATION', 'firefly.enums.ProblemType.ANOMALY_DETECTION']


class Estimator(Enum):
    LIGHT_GRADIENT_BOOSTING = 'light_gradient_boosting'
    LIBSVM_SVR = 'libsvm_svr'
    ADABOOST = 'adaboost'
    XGRADIENT_BOOSTING = 'xgradient_boosting'
    RANSAC = 'ransac'
    LARS = 'lars'
    LIBLINEAR_SVR = 'liblinear_svr'
    K_NEAREST_NEIGHBORS = 'k_nearest_neighbors'
    RANDOM_FOREST = 'random_forest'
    BERNOULLI_NB = 'bernoulli_nb'
    LOGREG = 'logreg'
    CAT_BOOST = 'cat_boost'
    ANOMALY_HIST = 'anomaly_hist'
    BAYESIAN_RIDGE = 'bayesian_ridge'
    GRADIENT_BOOSTING = 'gradient_boosting'
    GAUSSIAN_PROCESS = 'gaussian_process'
    LIBLINEAR_SVC = 'liblinear_svc'
    MULTINOMIAL_NB = 'multinomial_nb'
    DECISION_TREE = 'decision_tree'
    EXPONENTIAL_SMOOTHING = 'exponential_smoothing'
    BART = 'bart'
    ANOMALY_GMM = 'anomaly_gmm'
    NN_KERAS_SEQUENTIAL = 'nn_keras_sequential'
    LDA = 'lda'
    PROJ_LOGIT = 'proj_logit'
    ELASTIC_NET = 'elastic_net'
    ARIMA = 'arima'
    SGD = 'sgd'
    QDA = 'qda'
    LIBSVM_SVC = 'libsvm_svc'
    EXTRA_TREES = 'extra_trees'
    COMPLEMENT_NB = 'complement_nb'
    RIDGE_REGRESSION = 'ridge_regression'
    GAUSSIAN_NB = 'gaussian_nb'
    RIDGE_CLASSIFICATION = 'ridge_classification'
    AVERAGE_ESTIMATOR = 'average_estimator'
    ANOMALY_ISOF = 'anomaly_isof'
    PASSIVE_AGGRESSIVE = 'passive_aggressive'


class FeatureType(Enum):
    CATEGORICAL = 'categorical'
    NUMERICAL = 'numerical'
    TEXT = 'text'
    DATETIME = 'datetime'


class TargetMetric(Enum):
    F1 = 'f1'
    F2 = 'f2'
    ACCURACY = 'accuracy'
    MAE = 'mae'
    NORMALIZED_MAE = 'normalized_mae'
    MEDIAN_AE = 'median_ae'
    MAPE = 'mape'
    RMSLE = 'rmsle'
    COST_METRIC = 'cost_metric'
    MSE = 'mse'
    RMSE = 'rmse'
    NORMALIZED_MSE = 'normalized_mse'
    MAE_DISCRETE = 'mae_discrete'
    RMSPE = 'rmspe'
    NORMALIZED_RMSE = 'normalized_rmse'
    RECALL_MACRO = 'recall_macro'
    NORMALIZED_GINI = 'normalized_gini'
    SIGNED_SUM = 'signed_sum'
    LOG_LOSS = 'log_loss'
    AUC = 'auc'
    R2 = 'r2'
    R1 = 'r1'
    JACCARD = 'jaccard'
    NORMALIZED_MUTUAL_INFO = 'normalized_mutual_info'


class InterpretabilityLevel(Enum):
    EXPLAINABLE = 2
    PRECISE = 0


class SplittingStrategy(Enum):
    STRATIFIED = 'stratified'
    SHUFFLED = 'shuffled'
    TIME_ORDER = 'time_order'

    @staticmethod
    def ALL_CLASSIFICATION():
        return [SplittingStrategy.STRATIFIED, SplittingStrategy.SHUFFLED, SplittingStrategy.TIME_ORDER]

    @staticmethod
    def ALL_CLASSIFICATION_TIMESERIES():
        return [SplittingStrategy.TIME_ORDER]

    @staticmethod
    def ALL_MULTIVARIATE_TIMESERIES():
        return [SplittingStrategy.TIME_ORDER]

    @staticmethod
    def ALL_ANOMALY():
        return [SplittingStrategy.STRATIFIED, SplittingStrategy.SHUFFLED, SplittingStrategy.TIME_ORDER]

    @staticmethod
    def ALL_REGRESSION():
        return [SplittingStrategy.TIME_ORDER, SplittingStrategy.SHUFFLED]

    @staticmethod
    def ALL_REGRESSION_TIMESERIES():
        return [SplittingStrategy.TIME_ORDER]


class ValidationStrategy(Enum):
    HOLDOUT = 'holdout'
    CROSS_VALIDATION = 'cv'


class CVStrategy(Enum):
    AVERAGE_MODELS = 'average_models'
    LAST_MODEL = 'last_model'


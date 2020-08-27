# defines the df.cohorts DataFrame accessor and associated methods

from pandas_flavor import register_dataframe_accessor

from .cohort_metrics import CohortAnalysisException, CohortMetrics


@register_dataframe_accessor("cohorts")
class CohortAnalysisAccessor:

    """
    Register DataFrame.cohorts accessor

    Provides methods that faciliate the setting of particular
    DataFrames as the clickstream or cohorts attributes of a
    cohort_analysis.CohortMetrics instance

    """

    def __init__(self, df):
        self._df = df

    def __repr__(self):
        return "DataFrame.cohorts (accessor for cohort_analysis methods)"

    def __str__(self):
        return self.__repr__()

    def set_as_clickstream(
        self,
        metrics: CohortMetrics,
        timestamp_col: str = "timestamp",
        user_id_col: str = "user_id",
    ):

        """
        Register DataFrame.cohorts.set_as_clickstream

        Sets the clickstream attribute of a supplied CohortMetrics
        instance to be a copy of the DataFrame on which this
        method is called

        INPUTS:
            metrics - a cohort_analysis.metrics.CohortMetrics instance

        KEYWORDS:
            timestamp_col = "timestamp"
            user_id_col = "user_id"

            If the DataFrame has different names for these columns,
            that can be indicated using these keywords

        """

        clickstream = self._df.copy()

        initial_value = metrics.clickstream

        if timestamp_col != "timestamp":
            clickstream.loc[:, "timestamp"] = self._df.loc[:, timestamp_col]

        if user_id_col != "user_id":
            clickstream.loc[:, "user_id"] = self._df.loc[:, user_id_col]

        metrics.clickstream = clickstream

        try:
            metrics.verify_clickstream()
        except CohortAnalysisException as error:
            metrics.clickstream = initial_value  # reset
            raise error  # raise the exception

        metrics.clickstream = clickstream[["timestamp", "user_id"]]

    def set_as_cohorts(
        self,
        metrics: CohortMetrics,
        user_id_col: str = "user_id",
        reference_timestamp_col: str = "reference_timestamp",
    ):

        """
        Register DataFrame.cohorts.set_as_cohorts

        Sets the cohorts attribute of a supplied CohortMetrics
        instance to be a copy of the DataFrame on which this
        method is called

        INPUTS:
            metrics - a cohort_analysis.metrics.CohortMetrics instance

        KEYWORDS:
            user_id_col = "user_id"
            reference_timestamp_col = "reference_timestamp"

            If the DataFrame has different names for these columns,
            that can be indicated using these keywords

        """

        cohorts_copy = self._df.copy()

        initial_value = metrics.cohorts

        if user_id_col != "user_id":
            cohorts_copy.loc[:, "user_id"] = self._df.loc[:, user_id_col]
            cohorts_copy = cohorts_copy.drop(user_id_col, axis="columns")

        if reference_timestamp_col != "reference_timestamp":
            cohorts_copy.loc[:, "reference_timestamp"] = self._df.loc[
                :, reference_timestamp_col
            ]
            cohorts_copy = cohorts_copy.drop(reference_timestamp_col, axis="columns")

        metrics.cohorts = cohorts_copy

        try:
            metrics.verify_cohorts()
        except CohortAnalysisException as error:
            metrics.cohorts = initial_value  # reset
            raise error  # raise the exception

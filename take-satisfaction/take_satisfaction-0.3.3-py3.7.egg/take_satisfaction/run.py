__author__ = 'Gabriel Salgado, Juliana Guamá, Milo Utsch e Rogers Damas'
__version__ = '0.3.3'

import typing as tp

from take_satisfaction.utils import CONTEXT
from take_satisfaction.utils import load_params
from take_satisfaction.utils import query_df
from take_satisfaction.utils import spark_to_pandas
from take_satisfaction.preprocess import remove_manual
from take_satisfaction.conversion import convert_scale
from take_satisfaction.calculation import calculate_satisfaction_rate


def run(sql_context: CONTEXT, start_date: str, end_date: str, bot_identity: str, category: str,
        **kwargs) -> tp.Dict[str, tp.Any]:
    """Run Take Satisfaction
    
    :param sql_context: Context for spark.
    :type sql_context: ``pyspark.sql.HiveContext``
    :param start_date: Beginning date to filter ("yyyy-mm-dd").
    :type start_date: ``str``
    :param end_date: Ending date to filter ("yyyy-mm-dd").
    :type end_date: ``str``
    :param bot_identity: Bot identity on database.
    :type bot_identity: ``str``
    :param category: Satisfaction Survey tracking name on database.
    :type category: ``str``
    :param kwargs: Parameters to overwrite configuration parameters.
    :type kwargs: ``any``
    :return: Parameters and results for MLFlow register.
    :rtype: ``dict`` from ``str`` to ``any``
    """
    params = load_params()
    params.update(kwargs)
    
    databricks_query = params['databricks_query']
    bot_events_answer_column = params['bot_events_answer_column']
    bot_events_quantities_column = params['bot_events_quantities_column']
    sp_df = query_df(sql_context,
                     databricks_query,
                     answer=bot_events_answer_column,
                     quantities=bot_events_quantities_column,
                     start_date=start_date,
                     end_date=end_date,
                     bot_identity=bot_identity,
                     category=category)
    scale_raw_df = spark_to_pandas(sp_df)
    
    scale_manual = params['scale_manual']
    similarity_threshold = params['similarity_threshold']
    preprocessed_df = remove_manual(scale_raw_df, scale_manual, similarity_threshold, bot_events_answer_column)
    
    scale_translations = params['scale_translations']
    converted_df = convert_scale(preprocessed_df, bot_events_answer_column, scale_translations, similarity_threshold)
    
    bot_satisfaction_level_column = params['bot_satisfaction_level_column']
    bot_satisfaction_quantity_column = params['bot_satisfaction_quantity_column']
    satisfaction_rate = calculate_satisfaction_rate(converted_df, bot_satisfaction_level_column,
                                                    bot_satisfaction_quantity_column)
    
    return {
        'params': params,
        'result': {
            'raw': {
                'scale': scale_raw_df
            },
            'primary': {
                'preprocessed': preprocessed_df
            },
            'features': {
                'converted': converted_df
            },
            'model_input': {
                'satisfaction_rate': satisfaction_rate
            },
        }
    }

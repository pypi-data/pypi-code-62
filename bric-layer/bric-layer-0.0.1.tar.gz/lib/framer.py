import pandas
import numpy


def cartesian_product_basic(left, right):
    return left.assign(key=1).merge(right.assign(key=1), on='key').drop('key', axis=1)


# TODO - add left_columns_list
def join_dfs(left, right, left_join_column, right_join_column, join_type='inner',
             right_columns_list=(), rsuffix='_ex', drop=False):
    left = left.set_index(left_join_column)
    right = right.set_index(right_join_column)

    # this returns the index as a column as well. No need to have it in the right_columns_list
    return left.join(right[right_columns_list], how=join_type, rsuffix=rsuffix).reset_index(drop=drop)


def group_by_flattened(dataframe, sort_by_list=(), group_by_list=(), aggregates=None, columns_list=()):
    flattened_df = dataframe.sort_values(by=sort_by_list).groupby(group_by_list, as_index=False).agg(aggregates)

    if columns_list:
        flattened_df.columns = columns_list
    return flattened_df


def cartesian_iterative(pools):
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    return [sum(x) for x in result]


def rename_columns(dataframe, column_map):
    return dataframe.rename(columns=column_map)


# TODO - put some settings here
def dataframe_to_json(dataframe, **params):
    if params:
        return dataframe.to_json(**params)
    return dataframe.to_json()


def dataframe_to_csv(dataframe, **params):
    if params:
        return dataframe.to_csv(**params)
    return dataframe.to_csv()


def dataframe_from_json(dataframe, **params):
    if params:
        return dataframe.read_json(**params)
    return dataframe.read_json()


def dataframe_from_csv(dataframe, **params):
    if params:
        return dataframe.read_csv(**params)
    return dataframe.read_csv()


# TODO - write own dataframe functions, instead of pandas
class Framer:
    def __init__(self, layer):
        self.pandas = pandas
        self.numpy = numpy

        for option, value in layer.config.pandas.items():
            self.pandas.set_option(option, value)

        # TODO - overwrite slow pandas functions with numpy

    rename_columns = rename_columns
    dataframe_to_json = dataframe_to_json
    dataframe_to_csv = dataframe_to_csv
    cartesian_product_basic = cartesian_product_basic
    join_dfs = join_dfs
    group_by_flattened = group_by_flattened
    cartesian_iterative = cartesian_iterative

    def reset_options(self):
        self.pandas.reset_options('all')

    def merge_lists_to_dataframe(self, *df_lists):
        new_list = []
        for i in df_lists:
            new_list.extend(i)
        dataframe = self.pandas.concat(new_list)
        return dataframe.reset_index(drop=True)

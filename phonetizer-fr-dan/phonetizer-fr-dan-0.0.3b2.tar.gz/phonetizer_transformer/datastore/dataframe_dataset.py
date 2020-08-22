from torchtext import data

class DataFrameDataset(data.Dataset):
    """Converts DataFrame to PyTorch compatible Dataset"""

    def __init__(self, df, ortho_field, phon_field, is_test=False, **kwargs):
        fields = [('ortho', ortho_field), ('phon', phon_field)]
        examples = []
        for i, row in df.iterrows():
            phon = row.phon if not is_test else None
            ortho = row.ortho
            examples.append(data.Example.fromlist([ortho, phon], fields))

        super().__init__(examples, fields, **kwargs)

    @staticmethod
    def sort_key(ex):
        return len(ex.ortho)

    @classmethod
    def splits(cls, ortho_field, phon_field, train_df, val_df=None, test_df=None, **kwargs):
        train_data, val_data, test_data = (None, None, None)

        if train_df is not None:
            train_data = cls(train_df.copy(), ortho_field, phon_field, **kwargs)
        if val_df is not None:
            val_data = cls(val_df.copy(), ortho_field, phon_field, **kwargs)
        if test_df is not None:
            test_data = cls(test_df.copy(), ortho_field, phon_field, True, **kwargs)

        return tuple(d for d in (train_data, val_data, test_data) if d is not None)

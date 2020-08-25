def boxplots(df, target):
    import matplotlib.pyplot as plt
    import seaborn as sns
    cols = df.columns
    obj_cols = []
    int_cols = []
    for o in cols:
        if df[o].dtypes == object:
            obj_cols.append(o)
        else:
            int_cols.append(o)

    for k in range(len(obj_cols)):
        x1 = df[obj_cols[k]].dropna()
        x2 = dict(x1.value_counts())
        names = list(x2.keys())
        if len(names) >= 20:
            pass
        else:
            try:
                sns.boxplot(x=x1, y=str(target), data=df)
                plt.show()
            except:
                pass
    for m in range(len(int_cols)):
        x1 = df[int_cols[m]].dropna()
        try:
            sns.boxplot(x=x1, data=df)
            plt.show()
        except:
            pass

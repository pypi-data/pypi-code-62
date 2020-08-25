def scatterplots(data, target):
    import matplotlib.pyplot as plt
    import pandas as pd
    cols = data.columns
    obj_cols = []
    int_cols = []
    for o in cols:
        if data[o].dtypes == object:
            obj_cols.append(o)
        else:
            int_cols.append(o)

    for k in range(len(obj_cols)):
        x1 = data[obj_cols[k]]
        x2 = dict(x1.value_counts())
        names = list(x2.keys())
        if len(names) >= 20:
            pass
        else:
            y1 = data[str(target)]
            df45 = pd.DataFrame([x1, y1]).T
            x = df45.dropna()
            x1 = x[obj_cols[k]]
            y1 = x[str(target)]
            try:
                plt.scatter(x1, y1, color='g')
                plt.xlabel(obj_cols[k])
                plt.ylabel(str(target))
                plt.show()
            except:
                pass
    for m in range(len(int_cols)):
        x1 = data[int_cols[m]]
        y1 = data[str(target)]
        df45 = pd.DataFrame([x1, y1]).T
        x = df45.dropna()
        x1 = x[int_cols[m]]
        y1 = x[str(target)]
        try:
            plt.scatter(x1, y1, color='g')
            plt.xlabel(int_cols[m])
            plt.ylabel(str(target))
            plt.show()
        except:
            pass





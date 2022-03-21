import os
import pandas as pd

INPUT_DIR = 'csv' + os.sep
INPUT_XLS = INPUT_DIR + 'CivilReport.xls'
INPUT_CSV = INPUT_DIR + 'koordinate.txt'


def get_input_df():
    def remove_m(x):
        return x.replace("m", "")

    df_xls = pd.read_excel(INPUT_XLS, header=None)
    df_csv = pd.read_csv(INPUT_CSV, delimiter="\t", header=None)
    df_csv.columns = [0, 5, 6, 7, 8]

    df_xls = df_xls.drop(df_xls.index[0:14])
    df_xls = df_xls.drop(df_xls.index[-2:])
    df_xls[2] = df_xls[2].apply(remove_m)
    df_xls[3] = df_xls[3].apply(remove_m)
    df_xls[[0, 2, 3]] = df_xls[[0, 2, 3]].apply(pd.to_numeric)

    df_xls = pd.merge(df_xls, df_csv,  how='left', on=0)
    df_xls = df_xls.sort_values([1, 2])
    df_xls[0] = list(range(1, len(df_xls) + 1))
    df_xls.reset_index(drop=True, inplace=True)

    return df_xls


if __name__ == '__main__':
    df = get_input_df()

    print(df.iloc[0:40, 0:6])

#print(df_xls.dtypes)

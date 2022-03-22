import os
import pandas as pd
from cls.statio import Statio

INPUT_DIR = 'csv' + os.sep
INPUT_XLS = INPUT_DIR + 'CivilReport.xls'
INPUT_CSV = INPUT_DIR + 'koordinate.txt'
CSV_DELIMITER = "\t"


def get_input_df():
    def has_valid_code(x):
        return not x.startswith(("(4", "(5", "(6", "(7", "(8"))

    df_xls = pd.read_excel(INPUT_XLS, header=None)
    df_csv = pd.read_csv(INPUT_CSV, delimiter=CSV_DELIMITER, header=None)
    df_csv.columns = [0, 5, 6, 7, 8]

    df_xls = tidy_excel(df_xls)

    df_xls = pd.merge(df_xls, df_csv, how='left', on=0)
    df_xls = df_xls[df_xls[4].apply(has_valid_code)]
    df_xls = df_xls.sort_values([1, 2])

    df_xls[0] = list(range(1, len(df_xls) + 1))
    df_xls.reset_index(drop=True, inplace=True)
    return df_xls


def tidy_excel(excel_df):
    def remove_m(x):
        return x.replace("m", "")

    excel_df = excel_df.drop(excel_df.index[0:14])
    excel_df = excel_df.drop(excel_df.index[-2:])
    excel_df[2] = excel_df[2].apply(remove_m)
    excel_df[3] = excel_df[3].apply(remove_m)
    excel_df[[0, 2, 3]] = excel_df[[0, 2, 3]].apply(pd.to_numeric)
    return excel_df


if __name__ == '__main__':
    df = get_input_df()

    tolerance = 10

    statio = None
    for row in df.itertuples():
        if not statio:
            statio = Statio(row[2], row[3], tolerance)
            statio.add_row(row)
            continue

        if statio.in_tolerance(row[2]):
            statio.add_row(row)
            if row[3] == 0:
                statio.set_final_name(row[2])
        else:
            statio.finalize()
            statio = Statio(row[2], row[3], tolerance)
            statio.add_row(row)

        #print(row)

    #print(df)

    #print(df.iloc[0:40, 0:6])
#print(df_xls.dtypes)

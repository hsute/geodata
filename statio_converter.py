import os
import pandas as pd
from glob import glob
from cls.tolerance_adapter import ToleranceAdapter
from cls.excel_writer import GeodataExcelWriter
from cls.config import Config


def get_input_df():
    def has_valid_code(x):
        return not x.startswith(("(4", "(5", "(6", "(7", "(8"))

    df_xls = pd.read_excel(Config.INPUT_XLS, header=None)
    df_csv = pd.read_csv(Config.INPUT_CSV, delimiter=Config.CSV_DELIMITER, header=None)
    df_csv.columns = [0, 5, 6, 7, 8]

    df_xls = tidy_excel(df_xls)

    df_xls = pd.merge(df_xls, df_csv, how='left', on=0)
    df_xls = df_xls[df_xls[4].apply(has_valid_code)]
    df_xls = df_xls.sort_values(1, ignore_index=True)
    return df_xls


def tidy_excel(excel_df):
    excel_df = excel_df.drop(excel_df.index[0:14])
    excel_df = excel_df.drop(excel_df.index[-2:])
    excel_df.replace({2: {'m': ''}, 3: {'m': ''}}, inplace=True, regex=True)
    excel_df = excel_df.astype({0: 'int64', 2: 'float64', 3: 'float64'})
    excel_df[4].replace({'(9909)9909': 'Točka terena'}, inplace=True)
    excel_df[4].replace({'\((\w| )+\)': ''}, inplace=True, regex=True)
    return excel_df


def finalize_df(final_df):
    final_df = final_df.sort_values([1, 2], ignore_index=True)
    final_df[0] = list(range(1, len(final_df) + 1))
    return final_df


def printdf(df):
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 10)
    print(df.iloc[0:80])
    exit()


if __name__ == '__main__':
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)

    for f in glob(Config.OUTPUT_DIR + '*'):
        os.remove(f)

    df = get_input_df()

    tolerance = 10
    river = 'Neretva'

    ta = ToleranceAdapter(df, tolerance)
    if tolerance > 0:
        ta.process_sec_statios()
        df = ta.get_df()
    df = finalize_df(df)

    statios = df[1].unique()
    for statio in statios:
        geodata_excel = GeodataExcelWriter(statio, river, statio in ta.get_sec_statios())
        geodata_excel.add_sheet(df[df[1].values == statio])
        geodata_excel.done_writing()

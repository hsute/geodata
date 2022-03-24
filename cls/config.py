import os


class Config:
    INPUT_DIR = 'input' + os.sep
    INPUT_XLS = INPUT_DIR + 'CivilReport.xls'
    INPUT_CSV = INPUT_DIR + 'koordinate.txt'
    OUTPUT_DIR = INPUT_DIR + 'output' + os.sep
    CSV_DELIMITER = "\t"
    NO_0 = 'BEZ0'


class ExcelConfig:
    XLS_TITLE = 'POPREČNI PROFIL NA STACIONAŽI {}'
    XLS_COL_A = 'Broj točke'
    XLS_COL_B = 'Udaljenost od osi vodotoka [m]'
    XLS_COL_C = 'Opis točke'
    XLS_COL_DEF = 'HTRS96/TM'
    XLS_COL_D = 'E [m]'
    XLS_COL_E = 'N [m]'
    XLS_COL_F = 'h [m.n.m.]'
    XLS_COL_GH = 'WGS84'
    XLS_COL_G = 'ϕ [deg]'
    XLS_COL_H = 'λ [deg]'

    cell_format = {
        'align': 'center',
        'border': 1
    }

    cell_decimal2_format = {
        'align': 'center',
        'num_format': '0.00',
        'border': 1
    }

    cell_decimal13_format = {
        'align': 'center',
        'num_format': '0.0000000000000',
        'border': 1
    }

    header_format = {
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'border': 2,
        'text_wrap': True
    }

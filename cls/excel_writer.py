import pandas as pd
from cls.config import Config, ExcelConfig


class GeodataExcelWriter:
    def __init__(self, statio, river, no_0=False):
        self.statio = statio
        self.file_name = "{} {} {}".format(river, statio, Config.NO_0) if no_0 else "{} {}".format(river, statio)
        self.xls_formatter = GeodataExcelFormatter(statio)
        self.xls_writer = pd.ExcelWriter(Config.OUTPUT_DIR + self.file_name + '.xlsx', engine='xlsxwriter')

    def add_sheet(self, df):

        df.to_excel(self.xls_writer, sheet_name=self.statio, startrow=4, index=False,
                    header=False, columns=[0, 2, 4, 5, 6, 3, 7, 8])

        self.xls_formatter.format_document(self.xls_writer)

    def done_writing(self):
        self.xls_writer.save()


class GeodataExcelFormatter:
    def __init__(self, name):
        self.name = name
        self.title = ExcelConfig.XLS_TITLE.format(name)

    def format_document(self, xls_writer):
        workbook = xls_writer.book
        worksheet = xls_writer.sheets[self.name]
        header_formatter = workbook.add_format(ExcelConfig.header_format)
        cell_formatter = workbook.add_format(ExcelConfig.cell_format)
        cell_dec2_formatter = workbook.add_format(ExcelConfig.cell_decimal2_format)

        worksheet.merge_range('A1:H1', self.title, header_formatter)
        worksheet.merge_range('A3:A4', ExcelConfig.XLS_COL_A, header_formatter)
        worksheet.merge_range('B3:B4', ExcelConfig.XLS_COL_B, header_formatter)
        worksheet.merge_range('C3:C4', ExcelConfig.XLS_COL_C, header_formatter)
        worksheet.merge_range('D3:F3', ExcelConfig.XLS_COL_DEF, header_formatter)
        worksheet.merge_range('G3:H3', ExcelConfig.XLS_COL_GH, header_formatter)
        worksheet.write(3, 3, ExcelConfig.XLS_COL_D, header_formatter)
        worksheet.write(3, 4, ExcelConfig.XLS_COL_E, header_formatter)
        worksheet.write(3, 5, ExcelConfig.XLS_COL_F, header_formatter)
        worksheet.write(3, 6, ExcelConfig.XLS_COL_G, header_formatter)
        worksheet.write(3, 7, ExcelConfig.XLS_COL_H, header_formatter)

        worksheet.set_column(0, 0, 10, cell_formatter)
        worksheet.set_column(1, 1, 15, cell_dec2_formatter)
        worksheet.set_column(2, 2, 15, cell_formatter)
        worksheet.set_column(3, 5, 15, cell_dec2_formatter)
        worksheet.set_column(6, 7, 20, workbook.add_format(ExcelConfig.cell_decimal13_format))


        worksheet.write(5, 11, 152.30, workbook.add_format({'num_format': '0.00'}))
        worksheet.write('L5', 2562.00, workbook.add_format({'border': 1, 'num_format': '0.00'}))

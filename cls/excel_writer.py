import pandas as pd
from cls.config import Config, ExcelConfig


class GeodataExcelWriter:
    def __init__(self, statio, river, no_0=False):
        self.statio = statio
        self.file_name = "{} {} {}".format(river, statio, Config.NO_0) if no_0 else "{} {}".format(river, statio)
        self.xls_writer = pd.ExcelWriter(Config.OUTPUT_DIR + self.file_name + '.xlsx', engine='xlsxwriter')

    def add_sheet(self, df):
        workbook = self.xls_writer.book
        sheet = workbook.add_worksheet(self.statio)
        sheet.set_landscape()
        cell_formatter = workbook.add_format(ExcelConfig.cell_format)
        cell_dec2_formatter = workbook.add_format(ExcelConfig.cell_decimal2_format)
        cell_dec13_formatter = workbook.add_format(ExcelConfig.cell_decimal13_format)

        self._format_header(workbook, sheet)
        sheet.set_column(0, 0, 7)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 5, 13)
        sheet.set_column(6, 7, 19)

        row_index = 4
        for i in range(len(df.index)):
            row = df.iloc[i, [0, 2, 4, 5, 6, 3, 7, 8]].to_list()
            sheet.write(row_index, 0, row[0], cell_formatter)
            sheet.write(row_index, 1, row[1], cell_dec2_formatter)
            sheet.write(row_index, 2, row[2], cell_formatter)
            sheet.write(row_index, 3, row[3], cell_dec2_formatter)
            sheet.write(row_index, 4, row[4], cell_dec2_formatter)
            sheet.write(row_index, 5, row[5], cell_dec2_formatter)
            sheet.write(row_index, 6, row[6], cell_dec13_formatter)
            sheet.write(row_index, 7, row[7], cell_dec13_formatter)
            row_index += 1

    def _format_header(self, workbook, sheet):
        header_formatter = workbook.add_format(ExcelConfig.header_format)
        sheet.merge_range('A1:H1', ExcelConfig.XLS_TITLE.format(self.statio), header_formatter)
        sheet.merge_range('A3:A4', ExcelConfig.XLS_COL_A, header_formatter)
        sheet.merge_range('B3:B4', ExcelConfig.XLS_COL_B, header_formatter)
        sheet.merge_range('C3:C4', ExcelConfig.XLS_COL_C, header_formatter)
        sheet.merge_range('D3:F3', ExcelConfig.XLS_COL_DEF, header_formatter)
        sheet.merge_range('G3:H3', ExcelConfig.XLS_COL_GH, header_formatter)
        sheet.write(3, 3, ExcelConfig.XLS_COL_D, header_formatter)
        sheet.write(3, 4, ExcelConfig.XLS_COL_E, header_formatter)
        sheet.write(3, 5, ExcelConfig.XLS_COL_F, header_formatter)
        sheet.write(3, 6, ExcelConfig.XLS_COL_G, header_formatter)
        sheet.write(3, 7, ExcelConfig.XLS_COL_H, header_formatter)

    def done_writing(self):
        self.xls_writer.save()

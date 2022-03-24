import pandas as pd
from cls.config import Config


class GeodataExcelWriter:
    def __init__(self, statio, river, no_0=False):
        self.statio = statio
        self.file_name = "{} {} {}".format(river, statio, Config.NO_0) if no_0 else "{} {}".format(river, statio)
        self.xls_formatter = GeodataExcelFormatter(statio)
        self.xls_writer = pd.ExcelWriter(Config.OUTPUT_DIR + self.file_name + '.xlsx', engine='xlsxwriter')

    def add_sheet(self, df):
        #df = pd.DataFrame(sheet.data)
        df.to_excel(self.xls_writer, sheet_name=self.statio, startrow=4, index=False,
                    header=False, columns=[0, 2, 4, 5, 6, 3, 7, 8])
        self.xls_formatter.format_document(self.xls_writer)

    def done_writing(self):
        self.xls_writer.save()


class GeodataExcelFormatter:
    def __init__(self, name):
        self.name = name
        self.title = Config.XLS_TITLE.format(name)
        self.cell_format = {
            'align': 'center',
            'border': 1
        }
        self.header_format = {
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        }
        self.row_format = {
            'border': 0
        }

    def format_document(self, xls_writer):
        workbook = xls_writer.book
        worksheet = xls_writer.sheets[self.name]
        cell_formatter = workbook.add_format(self.cell_format)
        header_formatter = workbook.add_format(self.header_format)
        row_formatter = workbook.add_format(self.row_format)

        worksheet.set_column(0, 5, 15, cell_formatter)
        worksheet.set_column(6, 7, 20, cell_formatter)
        worksheet.set_row(1, None, row_formatter)
        worksheet.set_row(101, None, row_formatter)

        worksheet.merge_range('A1:H1', self.title, header_formatter)
        worksheet.merge_range('A3:A4', Config.XLS_COL_A, header_formatter)
        worksheet.merge_range('B3:B4', Config.XLS_COL_B, header_formatter)
        worksheet.merge_range('C3:C4', Config.XLS_COL_C, header_formatter)
        worksheet.merge_range('D3:F3', Config.XLS_COL_DEF, header_formatter)
        worksheet.merge_range('G3:H3', Config.XLS_COL_GH, header_formatter)
        worksheet.write(3, 3, Config.XLS_COL_D, header_formatter)
        worksheet.write(3, 4, Config.XLS_COL_E, header_formatter)
        worksheet.write(3, 5, Config.XLS_COL_F, header_formatter)
        worksheet.write(3, 6, Config.XLS_COL_G, header_formatter)
        worksheet.write(3, 7, Config.XLS_COL_H, header_formatter)

        worksheet.write_number('K5', 152.30, workbook.add_format({'num_format': '0.00'}))
        worksheet.write_number('L5', 2562.00, workbook.add_format({'border': 1, 'num_format': '0.00'}))

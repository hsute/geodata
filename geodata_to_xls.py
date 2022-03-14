import os
import csv
import pandas as pd

CSV_DIR = 'csv/'
XLS_DIR = CSV_DIR + 'xls/'
CR_FILE = CSV_DIR + 'report.csv'
CSV_DELIMITER = ';'


class GeodataExcelWriter:
    def __init__(self, name):
        self.xls_formatter = GeodataExcelFormatter(name)
        self.xls_writer = pd.ExcelWriter(XLS_DIR + name + '.xlsx', engine='xlsxwriter')

    def add_sheet(self, sheet):
        df = pd.DataFrame(sheet.data)
        df.to_excel(self.xls_writer, sheet_name=sheet.name, startrow=4, index=False, header=False)
        self.xls_formatter.format_document(self.xls_writer)

    def done_writing(self):
        self.xls_writer.save()


class GeodataExcelFormatter:
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

    def __init__(self, name):
        self.name = name
        self.title = self.XLS_TITLE.format(name)
        self.cell_format = {
            'align': 'center'
        }
        self.header_format = {
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        }

    def format_document(self, xls_writer):
        workbook = xls_writer.book
        worksheet = xls_writer.sheets[self.name]
        cell_formatter = workbook.add_format(self.cell_format)
        header_formatter = workbook.add_format(self.header_format)

        worksheet.set_column(0, 5, 15, cell_formatter)
        worksheet.set_column(6, 7, 20, cell_formatter)
        worksheet.merge_range('A1:H1', self.title, header_formatter)
        worksheet.merge_range('A3:A4', self.XLS_COL_A, header_formatter)
        worksheet.merge_range('B3:B4', self.XLS_COL_B, header_formatter)
        worksheet.merge_range('C3:C4', self.XLS_COL_C, header_formatter)
        worksheet.merge_range('D3:F3', self.XLS_COL_DEF, header_formatter)
        worksheet.merge_range('G3:H3', self.XLS_COL_GH, header_formatter)
        worksheet.write(3, 3, self.XLS_COL_D, header_formatter)
        worksheet.write(3, 4, self.XLS_COL_E, header_formatter)
        worksheet.write(3, 5, self.XLS_COL_F, header_formatter)
        worksheet.write(3, 6, self.XLS_COL_G, header_formatter)
        worksheet.write(3, 7, self.XLS_COL_H, header_formatter)


class XlsSheet:
    def __init__(self, name):
        self.name = name
        self.data = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}

    def add_row(self, csv_row):
        eu_notion_row = self.convert_row(csv_row)
        for index, value in enumerate(eu_notion_row):
            self.data[index].append(value)

    def convert_row(self, raw_row):
        return [
            raw_row[0],
            self.convert_us2eu_numbers(raw_row[1], 2),
            raw_row[2],
            self.convert_us2eu_numbers(raw_row[3], 2),
            self.convert_us2eu_numbers(raw_row[4], 2),
            self.convert_us2eu_numbers(raw_row[5], 2),
            self.convert_us2eu_numbers(raw_row[6], 13),
            self.convert_us2eu_numbers(raw_row[7], 13),
        ]

    @staticmethod
    def convert_us2eu_numbers(value, decimals):
        return format(round(float(value), decimals), '.{}f'.format(decimals)).replace('.', ',')


if __name__ == '__main__':
    if not os.path.exists(XLS_DIR):
        os.makedirs(XLS_DIR)

    try:
        with open(CR_FILE, newline='') as cr:
            cr_reader = csv.reader(cr, delimiter=CSV_DELIMITER)
            xls_sheet = None
            geo_xls = None

            for row in cr_reader:
                statio = row.pop(0)
                if statio == 'Station':
                    continue
                if not geo_xls or (xls_sheet.name != statio):
                    if geo_xls:
                        geo_xls.add_sheet(xls_sheet)
                        geo_xls.done_writing()

                    geo_xls = GeodataExcelWriter(statio)
                    xls_sheet = XlsSheet(statio)

                xls_sheet.add_row(row)
    except FileNotFoundError:
        print('Nije pronadjena datoteka {}!'.format(CR_FILE))

import os
import csv
import pandas as pd

CSV_DIR = 'csv/'
CR_FILE = CSV_DIR + 'report.csv'
CSV_DELIMITER = ';'


class GeodataExcelWriter:
    XLS_DIR = CSV_DIR + 'xls/'
    XLS_COL1 = 'Broj točke'
    XLS_COL2 = 'Udaljenost od osi vodotoka [m]'
    XLS_COL3 = 'Opis točke'
    XLS_COL456 = 'HTRS96/TM'
    XLS_COL4 = 'E [m]'
    XLS_COL5 = 'N [m]'
    XLS_COL6 = 'h [m.n.m.]'
    XLS_COL78 = 'WGS84'
    XLS_COL7 = 'ϕ [deg]'
    XLS_COL8 = 'λ [deg]'

    def __init__(self, name):
        self.name = name
        self.xls_writer = pd.ExcelWriter(self.XLS_DIR + name + '.xlsx', engine='xlsxwriter')
        self.title = 'POPREČNI PROFIL NA STACIONAŽI {}'.format(name)

    def add_sheet(self, sheet):
        df = pd.DataFrame(sheet.data)
        df.to_excel(self.xls_writer, sheet_name=self.name, startrow=4, index=False, header=False)
        self.format_document()

    def format_document(self):
        workbook = self.xls_writer.book
        worksheet = self.xls_writer.sheets[self.name]

        cell_format = workbook.add_format({
            'align': 'center'
        })
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })

        worksheet.set_column(0, 5, 15, cell_format)
        worksheet.set_column(6, 7, 20, cell_format)
        worksheet.merge_range('A1:H1', self.title, header_format)
        worksheet.merge_range('A3:A4', self.XLS_COL1, header_format)
        worksheet.merge_range('B3:B4', self.XLS_COL2, header_format)
        worksheet.merge_range('C3:C4', self.XLS_COL3, header_format)
        worksheet.merge_range('D3:F3', self.XLS_COL456, header_format)
        worksheet.merge_range('G3:H3', self.XLS_COL456, header_format)
        worksheet.write(3, 3, self.XLS_COL4, header_format)
        worksheet.write(3, 4, self.XLS_COL5, header_format)
        worksheet.write(3, 5, self.XLS_COL6, header_format)
        worksheet.write(3, 6, self.XLS_COL7, header_format)
        worksheet.write(3, 7, self.XLS_COL8, header_format)

    def done_writing(self):
        self.xls_writer.save()


class XlsSheet:
    def __init__(self, name):
        self.name = name
        self.data = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}

    def add_row(self, csv_row):
        eu_notion_row = self.convert_numbers(csv_row)
        for index, value in enumerate(eu_notion_row):
            self.data[index].append(value)

    @staticmethod
    def convert_numbers(raw_row):
        return [
            raw_row[0],
            format(round(float(raw_row[1]), 2), '.2f').replace('.', ','),
            raw_row[2],
            format(round(float(raw_row[3]), 2), '.2f').replace('.', ','),
            format(round(float(raw_row[4]), 2), '.2f').replace('.', ','),
            format(round(float(raw_row[5]), 2), '.2f').replace('.', ','),
            format(round(float(raw_row[6]), 13), '.13f').replace('.', ','),
            format(round(float(raw_row[7]), 13), '.13f').replace('.', ',')
        ]


if __name__ == '__main__':
    if not os.path.exists(CSV_DIR):
        os.makedirs(GeodataExcelWriter.XLS_DIR)

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

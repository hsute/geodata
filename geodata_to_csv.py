import os
import csv


class GeodataCSVProcessor:

    def __init__(self):
        self.write_csv_fh = None
        self.current_statio = None
        self.csv_writer = None
        self.title = 'POPREČNI PROFIL NA STACIONAŽI {}'

    def new_statio(self, statio):
        if self.write_csv_fh:
            self.write_csv_fh.close()

        self.current_statio = statio
        self.write_csv_fh = open(CSV_OUTPUT + statio + '.csv', 'w')
        self.csv_writer = csv.writer(self.write_csv_fh, delimiter=CSV_DELIMITER, lineterminator='\n')
        self.csv_writer.writerow([self.title.format(self.current_statio)])

    def write_row(self, row):
        self.csv_writer.writerow(row)


CSV_DIR = 'csv/'
CSV_OUTPUT = CSV_DIR + 'output/'
CR_FILE = CSV_DIR + 'CivilReport.csv'
CSV_DELIMITER = ';'


def convert_numbers(raw_row):
    return [
        row[0],
        format(round(float(row[1]), 2), '.2f').replace('.', ','),
        row[2],
        format(round(float(row[3]), 2), '.2f').replace('.', ','),
        format(round(float(row[4]), 2), '.2f').replace('.', ','),
        format(round(float(row[5]), 2), '.2f').replace('.', ',')
        ]


if __name__ == '__main__':
    if not os.path.exists(CSV_OUTPUT):
        os.mkdir(CSV_OUTPUT)

    with open(CR_FILE, newline='') as cr:
        cr_reader = csv.reader(cr, delimiter=CSV_DELIMITER)
        geo_proc = GeodataCSVProcessor()
        for row in cr_reader:
            statio = row.pop(0)
            if geo_proc.current_statio != statio:
                geo_proc.new_statio(statio)
            conv_row = convert_numbers(row)
            geo_proc.write_row(conv_row)

        geo_proc.write_csv_fh.close()

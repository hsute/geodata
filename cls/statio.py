import pandas as pd


class Statio:

    def __init__(self, statio, offset, tolerance=0):
        self.tolerance = tolerance
        self.name = statio
        self.meter = self._calculate_meters(statio)
        self.offset = offset
        self.df = None

    @staticmethod
    def _calculate_meters(statio):
        [km, m] = statio.split('+')
        return float(km) * 1000 + float(m)

    def in_tolerance(self, statio):
        statio_m = self._calculate_meters(statio)
        return self.meter - self.tolerance <= statio_m <= self.meter + self.tolerance

    def set_final_name(self, statio):
        self.name = statio
        self.meter = self._calculate_meters(statio)
        self.offset = 0

    def add_row(self, row):
        df_row = [{0: row[1], 1: row[3], 2: row[5], 3: row[6], 4: row[7], 5: row[4], 6: row[8], 7: row[9]}]
        new_df = pd.DataFrame(df_row)
        if self.df is None:
            self.df = new_df
        else:
            self.df = pd.concat([self.df, new_df], ignore_index=True)

    def finalize(self):
        # sortiraj df i isprintaj u xls
        self.df = self.df.sort_values([1])

        #print(self.df.iloc[0:40, 0:6])
        print(self.df)

        exit()

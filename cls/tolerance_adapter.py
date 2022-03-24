import numpy


class ToleranceAdapter:
    def __init__(self, df, tolerance):
        self.df = df
        self.tolerance = tolerance
        self.main_statios = self.df[self.df[2] == 0][1].unique()
        self.secondary_statios = self._get_secondary_statios()

    def process_sec_statios(self):
        for sec_statio in self.secondary_statios:
            for main_statio in self.main_statios:
                in_tolerance, stop_checking = self._in_tolerance(sec_statio, main_statio)
                if in_tolerance:
                    self._adapt_sec_statio(sec_statio, main_statio)
                    break

                if stop_checking:
                    break

    def get_df(self):
        return self.df

    def get_sec_statios(self):
        return self.secondary_statios

    def _get_secondary_statios(self):
        all_statios = self.df[1].unique()
        return numpy.setdiff1d(all_statios, self.main_statios, assume_unique=True)

    def _in_tolerance(self, sec_statio, main_statio):
        sec_meter = ToleranceAdapter._get_meters(sec_statio)
        main_meter = ToleranceAdapter._get_meters(main_statio)
        return [main_meter - self.tolerance <= sec_meter <= main_meter + self.tolerance,
                main_meter - sec_meter > self.tolerance]

    @staticmethod
    def _get_meters(statio):
        return float(statio.replace("+", ""))

    def _adapt_sec_statio(self, sec_statio, main_statio):
        to_change = self.df[self.df[1].values == sec_statio]
        self.df.iloc[to_change.index.values, [1]] = main_statio


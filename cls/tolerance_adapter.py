import numpy


class ToleranceAdapter:
    def __init__(self, df, tolerance):
        self.df = df
        self.tolerance = tolerance
        self.main_statios = self.df[self.df[2] == 0][1].unique()
        self.secondary_statios = self._get_secondary_statios()

    """
    Samo za ovaj algoritam mi je bitno da su glavne (offset=0) i sporedne 
    stacionaze sortirane, da bi se skratilo nepotrebno iteriranje.
    """
    def process_sec_statios(self):
        sec_sorted = self._sort_statios(self.secondary_statios)
        main_sorted = self._sort_statios(self.main_statios)
        for sec_meter, sec_statio in sec_sorted:
            for main_meter, main_statio in main_sorted:
                in_tolerance, stop_checking = self._in_tolerance(sec_meter, main_meter)
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

    def _in_tolerance(self, sec_meter, main_meter):
        return [main_meter - self.tolerance <= sec_meter <= main_meter + self.tolerance,
                main_meter - sec_meter > self.tolerance]

    @staticmethod
    def _get_meters(statio):
        return float(statio.replace("+", ""))

    def _adapt_sec_statio(self, sec_statio, main_statio):
        to_change = self.df[self.df[1].values == sec_statio]
        self.df.iloc[to_change.index.values, [1]] = main_statio

    def _sort_statios(self, statios):
        statio_dict = {}
        for statio in statios:
            statio_dict[self._get_meters(statio)] = statio
        return sorted(statio_dict.items())


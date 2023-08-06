import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
import os, time
from .data_structure import *
from .baseline_estimator import *
from .regressor import *
from .visualizer import *

URL_ROOT = 'https://raw.githubusercontent.com/tamu-engineering-research/COVID-EMDA/master/data_release/'
FOLDER_ROOT = '../data/data_archive/'
AREA_MAPPING = pd.DataFrame([
    # caiso
    ['caiso', 'caiso', 'rto', 'demand',   'caiso/caiso_rto_load.csv'],
    ['caiso', 'caiso', 'rto', 'genmix',   'caiso/caiso_rto_genmix.csv'],
    ['caiso', 'caiso', 'rto', 'price',    'caiso/caiso_rto_lmp.csv'],
    ['caiso', 'caiso', 'rto', 'weather',  'caiso/caiso_rto_weather.csv'],
    ['caiso', 'caiso', 'rto', 'covid',    'caiso/caiso_rto_covid.csv'],
    ['la',    'caiso', 'la',  'demand',   'caiso/caiso_la_load.csv'],
    ['la',    'caiso', 'la',  'weather',  'caiso/caiso_la_weather.csv'],
    ['la',    'caiso', 'la',  'covid',    'caiso/caiso_la_covid.csv'],
    ['la',    'caiso', 'la',  'patterns', 'caiso/caiso_la_patterns.csv'],
    ['la',    'caiso', 'la',  'social_distancing', 'caiso/caiso_la_social_distancing.csv'],
    # miso
    ['miso',         'miso',  'rto',     'demand',  'miso/miso_rto_load.csv'],
    ['miso',         'miso',  'rto',     'genmix',  'miso/miso_rto_genmix.csv'],
    ['miso',         'miso',  'rto',     'price',   'miso/miso_rto_lmp.csv'],
    ['miso',         'miso',  'rto',     'weather', 'miso/miso_rto_weather.csv'],
    ['miso',         'miso',  'rto',     'covid',   'miso/miso_rto_covid.csv'],
    ['miso_north',   'miso',  'north',   'demand',  'miso/miso_north_load.csv'],
    ['miso_north',   'miso',  'north',   'weather', 'miso/miso_north_weather.csv'],
    ['miso_central', 'miso',  'central', 'demand',  'miso/miso_central_load.csv'],
    ['miso_central', 'miso',  'central', 'weather', 'miso/miso_central_weather.csv'],
    ['miso_south',   'miso',  'south',   'demand',  'miso/miso_south_load.csv'],
    ['miso_south',   'miso',  'south',   'weather', 'miso/miso_south_weather.csv'],
    # isone
    ['isone',  'isone', 'rto',    'demand',   'isone/isone_rto_load.csv'],
    ['isone',  'isone', 'rto',    'genmix',   'isone/isone_rto_genmix.csv'],
    ['isone',  'isone', 'rto',    'price',    'isone/isone_rto_lmp.csv'],
    ['isone',  'isone', 'rto',    'weather',  'isone/isone_rto_weather.csv'],
    ['isone',  'isone', 'rto',    'covid',    'isone/isone_rto_covid.csv'],
    ['boston', 'isone', 'boston', 'demand',   'isone/isone_boston_load.csv'],
    ['boston', 'isone', 'boston', 'price',    'isone/isone_boston_lmp.csv'],
    ['boston', 'isone', 'boston', 'weather',  'isone/isone_boston_weather.csv'],
    ['boston', 'isone', 'boston', 'covid',    'isone/isone_boston_covid.csv'],
    ['boston', 'isone', 'boston', 'patterns', 'isone/isone_boston_patterns.csv'],
    ['boston', 'isone', 'boston', 'social_distancing', 'isone/isone_boston_social_distancing.csv'],
    # nyiso
    ['nyiso', 'nyiso', 'rto', 'demand',   'nyiso/nyiso_rto_load.csv'],
    ['nyiso', 'nyiso', 'rto', 'genmix',   'nyiso/nyiso_rto_genmix.csv'],
    ['nyiso', 'nyiso', 'rto', 'price',    'nyiso/nyiso_rto_lmp.csv'],
    ['nyiso', 'nyiso', 'rto', 'weather',  'nyiso/nyiso_rto_weather.csv'],
    ['nyiso', 'nyiso', 'rto', 'covid',    'nyiso/nyiso_rto_covid.csv'],
    ['nyc',   'nyiso', 'nyc', 'demand',   'nyiso/nyiso_nyc_load.csv'],
    ['nyc',   'nyiso', 'nyc', 'price',    'nyiso/nyiso_nyc_lmp.csv'],
    ['nyc',   'nyiso', 'nyc', 'weather',  'nyiso/nyiso_nyc_weather.csv'],
    ['nyc',   'nyiso', 'nyc', 'covid',    'nyiso/nyiso_nyc_covid.csv'],
    ['nyc',   'nyiso', 'nyc', 'patterns', 'nyiso/nyiso_nyc_patterns.csv'],
    ['nyc',   'nyiso', 'nyc', 'social_distancing', 'nyiso/nyiso_nyc_social_distancing.csv'],
    # pjm
    ['pjm',     'pjm', 'rto',     'demand',   'pjm/pjm_rto_load.csv'],
    ['pjm',     'pjm', 'rto',     'genmix',   'pjm/pjm_rto_genmix.csv'],
    ['pjm',     'pjm', 'rto',     'price',    'pjm/pjm_rto_lmp.csv'],
    ['pjm',     'pjm', 'rto',     'weather',  'pjm/pjm_rto_weather.csv'],
    ['pjm',     'pjm', 'rto',     'covid',    'pjm/pjm_rto_covid.csv'],
    ['chicago', 'pjm', 'chicago', 'demand',   'pjm/pjm_chicago_load.csv'],
    ['chicago', 'pjm', 'chicago', 'price',    'pjm/pjm_chicago_lmp.csv'],
    ['chicago', 'pjm', 'chicago', 'weather',  'pjm/pjm_chicago_weather.csv'],
    ['chicago', 'pjm', 'chicago', 'covid',    'pjm/pjm_chicago_covid.csv'],
    ['chicago', 'pjm', 'chicago', 'patterns', 'pjm/pjm_chicago_patterns.csv'],
    ['chicago', 'pjm', 'chicago', 'social_distancing', 'pjm/pjm_chicago_social_distancing.csv'],
    ['phila',   'pjm', 'phila',   'demand',   'pjm/pjm_phila_load.csv'],
    ['phila',   'pjm', 'phila',   'price',    'pjm/pjm_phila_lmp.csv'],
    ['phila',   'pjm', 'phila',   'weather',  'pjm/pjm_phila_weather.csv'],
    ['phila',   'pjm', 'phila',   'covid',    'pjm/pjm_phila_covid.csv'],
    ['phila',   'pjm', 'phila',   'patterns', 'pjm/pjm_phila_patterns.csv'],
    ['phila',   'pjm', 'phila',   'social_distancing', 'pjm/pjm_phila_social_distancing.csv'],
    # spp
    ['spp',       'spp', 'rto',   'demand',   'spp/spp_rto_load.csv'],
    ['spp',       'spp', 'rto',   'genmix',   'spp/spp_rto_genmix.csv'],
    ['spp',       'spp', 'rto',   'price',    'spp/spp_rto_lmp.csv'],
    ['spp',       'spp', 'rto',   'weather',  'spp/spp_rto_weather.csv'],
    ['spp',       'spp', 'rto',   'covid',    'spp/spp_rto_covid.csv'],
    ['spp_north', 'spp', 'north', 'demand',   'spp/spp_north_load.csv'],
    ['spp_north', 'spp', 'north', 'weather',  'spp/spp_north_weather.csv'],
    ['spp_south', 'spp', 'south', 'demand',   'spp/spp_south_load.csv'],
    ['spp_south', 'spp', 'south', 'weather',  'spp/spp_south_weather.csv'],
    ['kck',       'spp', 'kck',   'demand',   'spp/spp_kck_load.csv'],
    ['kck',       'spp', 'kck',   'price',    'spp/spp_kck_lmp.csv'],
    ['kck',       'spp', 'kck',   'weather',  'spp/spp_kck_weather.csv'],
    ['kck',       'spp', 'kck',   'covid',    'spp/spp_kck_covid.csv'],
    ['kck',       'spp', 'kck',   'patterns', 'spp/spp_kck_patterns.csv'],
    ['kck',       'spp', 'kck',   'social_distancing', 'spp/spp_kck_social_distancing.csv'],
    # ercot
    ['ercot',   'ercot', 'rto',     'demand',   'ercot/ercot_rto_load.csv'],
    ['ercot',   'ercot', 'rto',     'genmix',   'ercot/ercot_rto_genmix.csv'],
    ['ercot',   'ercot', 'rto',     'price',    'ercot/ercot_rto_lmp.csv'],
    ['ercot',   'ercot', 'rto',     'weather',  'ercot/ercot_rto_weather.csv'],
    ['ercot',   'ercot', 'rto',     'covid',    'ercot/ercot_rto_covid.csv'],
    ['houston', 'ercot', 'houston', 'demand',   'ercot/ercot_houston_load.csv'],
    ['houston', 'ercot', 'houston', 'price',    'ercot/ercot_houston_lmp.csv'],
    ['houston', 'ercot', 'houston', 'weather',  'ercot/ercot_houston_weather.csv'],
    ['houston', 'ercot', 'houston', 'covid',    'ercot/ercot_houston_covid.csv'],
    ['houston', 'ercot', 'houston', 'patterns', 'ercot/ercot_houston_patterns.csv'],
    ['houston', 'ercot', 'houston', 'social_distancing', 'ercot/ercot_houston_social_distancing.csv'],
], columns=['keyword', 'market', 'region', 'kind', 'file']).set_index('keyword')
BIG_EVENTS_US = [
    ('first_case_in_us',         pd.to_datetime('2020-01-20')),
    ('state_of_emergency_in_us', pd.to_datetime('2020-03-13')),
    ('over_100k_case_in_us',     pd.to_datetime('2020-03-29')),
    ('over_1m_case_in_us',       pd.to_datetime('2020-04-29')),
    ('over_5m_case_in_us',       pd.to_datetime('2020-08-09')),
    ('over_10m_case_in_us',      pd.to_datetime('2020-11-09')),
]
BIG_EVENTS_REGION = {
    'CA': [('state_of_emergency_in_california', pd.to_datetime('2020-03-02'))],
    'NY': [('state_of_emergency_in_new_york', pd.to_datetime('2020-03-07'))],
    'NE': [('state_of_emergency_in_new_england', pd.to_datetime('2020-03-13'))],  # last date in this area
    'IL': [('state_of_emergency_in_illinois', pd.to_datetime('2020-03-09'))],
    'PA': [('state_of_emergency_in_pennsylvania', pd.to_datetime('2020-03-19'))],
    'KS': [('state_of_emergency_in_kansas', pd.to_datetime('2020-03-12'))],
    'MI': [('state_of_emergency_in_missouri', pd.to_datetime('2020-03-13'))],
    'TX': [('state_of_emergency_in_texas', pd.to_datetime('2020-03-13'))],  # specifically, state of disaster
}
BIG_EVENTS_MAPPING = {
    'caiso':   dict(BIG_EVENTS_US + BIG_EVENTS_REGION['CA']),
    'la':      dict(BIG_EVENTS_US + BIG_EVENTS_REGION['CA']),
    'miso':    dict(BIG_EVENTS_US + BIG_EVENTS_REGION['IL']),
    'isone':   dict(BIG_EVENTS_US + BIG_EVENTS_REGION['NE']),
    'boston':  dict(BIG_EVENTS_US + BIG_EVENTS_REGION['NE']),
    'nyiso':   dict(BIG_EVENTS_US + BIG_EVENTS_REGION['NY']),
    'nyc':     dict(BIG_EVENTS_US + BIG_EVENTS_REGION['NY']),
    'pjm':     dict(BIG_EVENTS_US + BIG_EVENTS_REGION['PA']),
    'chicago': dict(BIG_EVENTS_US + BIG_EVENTS_REGION['IL']),
    'phila':   dict(BIG_EVENTS_US + BIG_EVENTS_REGION['PA']),
    'spp':     dict(BIG_EVENTS_US + BIG_EVENTS_REGION['KS']),
    'kck':     dict(BIG_EVENTS_US + BIG_EVENTS_REGION['KS']),
    'ercot':   dict(BIG_EVENTS_US + BIG_EVENTS_REGION['TX']),
    'houston': dict(BIG_EVENTS_US + BIG_EVENTS_REGION['TX']),
}
MOBILITY_KEYWORD = {
    'retail':          'Retail',
    'grocery':         'Grocery_Pharmacy',
    'restaurant':      'Restaurant_Recreaction',
    'completely_home': 'completely_home_device_count',
    'median_home':     'median_home_dwell_time',
    'part_time_work':  'part_time_work_behavior_devices',
    'full_time_work':  'full_time_work_behavior_devices',
}
HIST_DATE_RANGE = pd.date_range('2017-01-01', '2019-12-31')
FIRST_CASE_DATE = pd.to_datetime('2020-01-20')
DATE_RANGE_OF_INTEREST = pd.date_range('2020-01-01', '2020-06-30')
LONG_DATE_RANGE_OF_INTEREST = pd.date_range('2017-01-01', '2020-06-30')


def download_online_data(area='all', folder='data_archive/', overwrite=False):  # might be slow
    assert isinstance(area, (str, tuple, list))
    assert isinstance(folder, str)
    assert isinstance(overwrite, bool)
    if not folder.endswith('/'):
        folder = folder + '/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    for mkt in ('caiso', 'miso', 'isone', 'nyiso', 'pjm', 'spp', 'ercot'):
        if not os.path.exists(folder + mkt):
            os.makedirs(folder + mkt)
    if area == 'all':
        area = AREA_MAPPING.index.unique()
    elif isinstance(area, str):
        area = (area,)
    for a in area:
        files = AREA_MAPPING.loc[a, 'file']
        for fn in files:
            for _ in range(5):  # at most 5 times
                try:
                    if os.path.exists(folder + fn) and (not overwrite):
                        print(f"Warning: Skip to avoid overwrite {fn}.")
                        break
                    print(f"Try downloading {fn}...")
                    data = urlopen(URL_ROOT + fn, timeout=300).read().decode('utf-8')
                    with open(folder + fn, 'w') as f:
                        f.write(data)
                    break
                except:
                    print(f"Fail to download {fn}.")
                    time.sleep(5)


def find_archive_folder(search_folder):
    def _check_folder_eligibility(root):
        check = np.sum([os.path.exists(root + fd) for fd in target_folders])
        if check == len(target_folders):
            return True
        elif 0 < check < len(target_folders):
            print(f"Warning: Find an incomplete data archive in {root}. Continue searching...")
        return False
    search_folder = handle_folder(search_folder)
    target_folders = ('caiso/', 'miso', 'isone', 'nyiso', 'pjm', 'spp', 'ercot')
    for root in ('../data/data_archive/', 'data/data_archive/', 'data_archive/', './'):  # most likely
        if _check_folder_eligibility(root) is True:
            return root  # only return the first one
    for root, _, _ in os.walk(search_folder):
        if _check_folder_eligibility(root) is True:
            return root
    return None  # return None when not found


class Area(object):
    def __init__(self, name, source='archive'):
        assert name in AREA_MAPPING.index.unique()
        assert source is None or isinstance(source, str)  # online or a folder path
        self.name = name
        if source == 'archive':  # auto completion
            source = find_archive_folder('../')
        if source == 'online':
            self.source = URL_ROOT + AREA_MAPPING.loc[self.name, 'file']
            self.source.index = AREA_MAPPING.loc[self.name, 'kind']
        elif os.path.exists(source):  # folder path
            self.source = handle_folder(source) + AREA_MAPPING.loc[self.name, 'file']
            self.source.index = AREA_MAPPING.loc[self.name, 'kind']
        else:
            self.source = None

    def archive_online_data(self, folder='data_archive/'):  # download data
        download_online_data(self.name, folder)


class RTO(Area):
    def __init__(self, name, source='archive'):
        super().__init__(name, source)
        self.dfmt_demand = DataFormatter('demand')  # explicit data management
        self.dfmt_genmix = DataFormatter('genmix')
        self.dfmt_price = DataFormatter('price')
        self.dfmt_weather = DataFormatter('weather')
        self.dfmt_mobility = DataFormatter('mobility')
        self.dfmt_covid = DataFormatter('covid')
        self.big_event = {}
        self._import_data()

    def _import_data(self):
        if self.source is not None:  # no mobility below
            self.dfmt_demand.import_from_source(self.source['demand'])
            self.dfmt_genmix.import_from_source(self.source['genmix'])
            self.dfmt_price.import_from_source(self.source['price'])
            self.dfmt_weather.import_from_source(self.source['weather'])
            self.dfmt_covid.import_from_source(self.source['covid'])
        if self.name in BIG_EVENTS_MAPPING.keys():
            self.big_event = BIG_EVENTS_MAPPING[self.name]
        return self

    # ::::: LOAD BASELINES ::::: #
    @staticmethod
    def _check_demand_baseline_inputs(date, method, shift_year, pickle_file):
        date = handle_date(date)
        assert method in ('date-alignment', 'week-alignment', 'backcast')
        assert isinstance(shift_year, int)
        assert pickle_file is None or isinstance(pickle_file, str)
        return date, method, shift_year, pickle_file

    def _init_demand_baseline(self, date, method, shift_year, pickle_file):
        if method == 'date-alignment':
            bl_da = DateAlignmentBaseline()
            bl_da.import_data(self.dfmt_demand)
            bl_da.import_target_date(date)
            bl_da.cal_baseline(shift_year)
            bl_da.get_observation()
            return bl_da
        elif method == 'week-alignment':
            bl_wa = WeekAlignmentBaseline()
            bl_wa.import_data(self.dfmt_demand)
            bl_wa.import_target_date(date)
            bl_wa.cal_baseline(shift_year)
            bl_wa.get_observation()
            return bl_wa
        else:  # backcast
            if pickle_file is None:
                pickle_file = find_pickle_file(
                    search_folder=os.path.dirname(os.getcwd()),
                    file_name=f"hourly-backcast-demand-{self.name}.pickle",
                )
            assert pickle_file is not None
            bl_bct = BackcastDemandBaseline().load(pickle_file)
            bl_bct.import_data(self.dfmt_weather, self.dfmt_demand)
            bl_bct.import_target_date(date)
            bl_bct.update_backcast_data()
            bl_bct.cal_baseline()
            bl_bct.get_observation()
            return bl_bct

    def cal_demand_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='date-alignment', shift_year=1, pickle_file=None):
        date, method, shift_year, pickle_file = \
            self._check_demand_baseline_inputs(date, method, shift_year, pickle_file)
        bl = self._init_demand_baseline(date, method, shift_year, pickle_file)
        return bl.baseline.data

    def eval_demand_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='date-alignment', shift_year=1, pickle_file=None):
        date, method, shift_year, pickle_file = \
            self._check_demand_baseline_inputs(date, method, shift_year, pickle_file)
        bl = self._init_demand_baseline(date, method, shift_year, pickle_file)
        mape, smape, rmse = bl.evaluate()
        return mape, smape, rmse

    def plot_demand_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='date-alignment', shift_year=1, pickle_file=None):
        date, method, shift_year, pickle_file = \
            self._check_demand_baseline_inputs(date, method, shift_year, pickle_file)
        bl = self._init_demand_baseline(date, method, shift_year, pickle_file)
        bl.plot()
        return bl

    # ::::: GENMIX BASELINES ::::: #
    @staticmethod
    def _check_genmix_baseline_inputs(date, method, kind, shift_year, verbose):
        date = handle_date(date)
        assert method in ('month-alignment', 'monthly-trend')
        assert kind in ('coal', 'gas', 'oil', 'nuclear', 'hydro', 'wind', 'solar', 'renewable')
        if kind == 'renewable':
            kind = ('hydro', 'wind', 'solar')
        assert isinstance(shift_year, int)
        assert isinstance(verbose, bool)
        return date, method, kind, shift_year, verbose

    def _init_genmix_baseline(self, date, method, kind, shift_year, verbose):
        if method == 'month-alignment':
            bl_moa = MonthAlignmentBaseline()
            bl_moa.import_data(self.dfmt_genmix.aggregate_by_kind(kind, np.sum))
            bl_moa.import_target_date(date)
            bl_moa.cal_baseline(shift_year)
            bl_moa.get_observation()
            return bl_moa
        else:  # monthly-trend'
            bl_mot = MonthlyTrendBaseline()
            bl_mot.import_data(self.dfmt_genmix.aggregate_by_kind(kind, np.sum))
            bl_mot.update_trend_data(HIST_DATE_RANGE, verbose)  #
            bl_mot.import_target_date(date)
            bl_mot.cal_baseline()
            bl_mot.get_observation()
            return bl_mot

    def cal_genmix_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='month-alignment', kind='renewable', shift_year=1, verbose=False):
        date, method, kind, shift_year, verbose = \
            self._check_genmix_baseline_inputs(date, method, kind, shift_year, verbose)
        bl = self._init_genmix_baseline(date, method, kind, shift_year, verbose)
        return bl.baseline.data

    def eval_genmix_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='month-alignment', kind='renewable', shift_year=1, verbose=False):
        date, method, kind, shift_year, verbose = \
            self._check_genmix_baseline_inputs(date, method, kind, shift_year, verbose)
        bl = self._init_genmix_baseline(date, method, kind, shift_year, verbose)
        mape, smape, rmse = bl.evaluate()
        return mape, smape, rmse

    def plot_genmix_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='month-alignment', kind='renewable', shift_year=1, verbose=False):
        date, method, kind, shift_year, verbose = \
            self._check_genmix_baseline_inputs(date, method, kind, shift_year, verbose)
        bl = self._init_genmix_baseline(date, method, kind, shift_year, verbose)
        bl.plot()
        return bl

    # ::::: PRICE BASELINES ::::: #
    @staticmethod
    def _check_price_baseline_inputs(date, method, hist_date_range):
        date = handle_date(date)
        assert method in ('distrib-index', 'distrib-dist')
        assert isinstance(hist_date_range, pd.DatetimeIndex)
        return date, method, hist_date_range

    def _init_price_baseline(self, date, method, hist_date_range):
        if method == 'distrib-index':
            bl_di = DistributionIndexBaseline()
            bl_di.import_data(self.dfmt_price)
            bl_di.update_fluc_index_data(hist_date_range)  # slow
            bl_di.import_target_date(date)
            bl_di.get_observation()
            bl_di.cal_baseline()
            return bl_di
        else:  # distrib-dist
            bl_dd = DistributionDistanceBaseline()
            bl_dd.import_data(self.dfmt_price)
            bl_dd.import_target_date(date)
            bl_dd.get_observation()
            bl_dd.cal_baseline()
            return bl_dd

    def cal_price_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='distrib-index', hist_date_range=HIST_DATE_RANGE):
        date, method, hist_date_range = self._check_price_baseline_inputs(date, method, hist_date_range)
        bl = self._init_price_baseline(date, method, hist_date_range)
        return bl.baseline.data

    def eval_price_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='distrib-index', hist_date_range=HIST_DATE_RANGE):
        date, method, hist_date_range = self._check_price_baseline_inputs(date, method, hist_date_range)
        bl = self._init_price_baseline(date, method, hist_date_range)
        mape, smape, rmse = bl.evaluate()
        return mape, smape, rmse

    def plot_price_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='distrib-index', hist_date_range=HIST_DATE_RANGE):
        date, method, hist_date_range = self._check_price_baseline_inputs(date, method, hist_date_range)
        bl = self._init_price_baseline(date, method, hist_date_range)
        bl.plot()
        return bl

    # ::::: MOBILITY BASELINES ::::: #
    def cal_mobility_baseline(self, *args, **kwargs):
        print('Warning: No mobility data in city level.')

    def eval_mobility_baseline(self, *args, **kwargs):
        print('Warning: No mobility data in city level.')

    def plot_mobility_baseline(self, *args, **kwargs):
        print('Warning: No mobility data in city level.')

    # ::::: REGRESSION ANALYSIS ::::: #
    def test_demand_correlation(self, date=DATE_RANGE_OF_INTEREST):  # regression: demand ~ tmpc + tmpc^2
        date = handle_date(date)
        ols = OrdinaryLeastSquares()
        tmpc = self.dfmt_weather.select_by_date(after=date[0], before=date[-1]).select_by_kind('tmpc').flatten()
        ols.train_x = merge_by_date({'tmpc': tmpc, 'tmpc2': tmpc ** 2}).data
        ols.train_y = self.dfmt_demand.select_by_date(after=date[0], before=date[-1]).flatten().data
        ols.train()
        return ols

    def test_price_correlation(self, date=DATE_RANGE_OF_INTEREST):  # regression: price ~ gas + demand + tmpc
        date = handle_date(date)
        ols = OrdinaryLeastSquares()
        gas = self.dfmt_genmix.select_by_date(after=date[0], before=date[-1]).select_by_kind('gas').flatten()
        dmd = self.dfmt_demand.select_by_date(after=date[0], before=date[-1]).flatten()
        tmpc = self.dfmt_weather.select_by_date(after=date[0], before=date[-1]).select_by_kind('tmpc').flatten()
        ols.train_x = merge_by_date({'gas': gas, 'demand': dmd, 'tmpc': tmpc}).data
        ols.train_y = self.dfmt_price.select_by_date(after=date[0], before=date[-1]).flatten().data
        ols.train()
        return ols

    @staticmethod
    def _check_regression_inputs(x, y, frac_train):
        assert isinstance(x, (list, dict, np.ndarray, pd.DataFrame, DataFormatter))
        assert isinstance(y, (list, dict, np.ndarray, pd.Series, DataFormatter))
        assert isinstance(frac_train, float) and 0 < frac_train <= 1
        if isinstance(x, (list, dict, np.ndarray)):
            x = pd.DataFrame(x)  # 2d
        elif isinstance(x, DataFormatter):
            x = x.flatten().data
        if isinstance(y, (list, dict, np.ndarray)):
            y = pd.Series(y)  # 1d, but compatible to 1d-like 2d
        elif isinstance(y, DataFormatter):
            y = y.flatten().data
            y = y[y.columns[0]]  # shrink to pd.Series
        assert len(x) == len(y)
        return x, y, frac_train

    @staticmethod
    def _split_regression_data(x, y, frac_train):
        n_train = int(len(x) * frac_train)
        train_x = x.iloc[:n_train, :]
        test_x = x.iloc[n_train:, :]
        train_y = y.iloc[:n_train]
        test_y = y.iloc[n_train:]
        return train_x, train_y, test_x, test_y

    def cal_correlation_coeff(self, x, y):
        x, y, frac_train = self._check_regression_inputs(x, y, 1.0)  # no test data
        train_x, train_y, test_x, test_y = self._split_regression_data(x, y, frac_train)
        ols = OrdinaryLeastSquares()
        ols.train_x, ols.train_y, ols.test_x, ols.test_y = train_x, train_y, test_x, test_y
        corr, _ = ols.cal_correlation_coeff()
        return corr

    def run_general_ols(self, x, y, ratio_train=0.7):
        x, y, ratio_train = self._check_regression_inputs(x, y, ratio_train)
        train_x, train_y, test_x, test_y = self._split_regression_data(x, y, ratio_train)
        ols = OrdinaryLeastSquares()
        ols.train_x, ols.train_y, ols.test_x, ols.test_y = train_x, train_y, test_x, test_y
        ols.train()
        ols.test()
        return ols

    def run_general_var(self, x, y, frac_train=0.7):
        x, y, frac_train = self._check_regression_inputs(x, y, frac_train)
        train_x, train_y, test_x, test_y = self._split_regression_data(x, y, frac_train)
        var = VectorAutoregression()
        var.train_x, var.train_y, var.test_x, var.test_y = train_x, train_y, test_x, test_y
        var.train()
        var.test()
        var.model_verification()
        var.impulse_response()
        var.variance_decomposition()
        return var

    # ::::: PLOTTERS ::::: #
    def plot_demand_series(self, date=DATE_RANGE_OF_INTEREST, mark_big_event=False, config=None):
        date = handle_date(date)
        assert isinstance(mark_big_event, bool)
        assert config is None or isinstance(config, dict)
        vs_dmd = DemandVisualizer()
        vs_dmd.import_data(self.dfmt_demand)
        vs_dmd.import_big_event(self.big_event)
        if config is not None:
            vs_dmd.import_config(config)
        vs_dmd.plot_demand_series(date, mark_big_event)
        return vs_dmd

    def plot_daily_demand_profile(self, date=DATE_RANGE_OF_INTEREST, config=None):
        date = handle_date(date)
        assert config is None or isinstance(config, dict)
        vs_dmd = DemandVisualizer()
        vs_dmd.import_data(self.dfmt_demand)
        vs_dmd.import_big_event(self.big_event)
        if config is not None:
            vs_dmd.import_config(config)
        vs_dmd.plot_daily_demand_profile(date)
        return vs_dmd

    def plot_generation_mix(self, date=LONG_DATE_RANGE_OF_INTEREST, duration='1M', config=None):
        date = handle_date(date)
        assert isinstance(duration, str)
        assert config is None or isinstance(config, dict)
        vs_gen = GenerationVisualizer()
        vs_gen.import_data(self.dfmt_genmix)
        if config is not None:
            vs_gen.import_config(config)
        vs_gen.plot_generation_mix(date, duration)
        return vs_gen

    def plot_renewable_share(
            self, date=LONG_DATE_RANGE_OF_INTEREST, kind=('hydro', 'solar', 'wind'), duration='1M', config=None):
        date = handle_date(date)
        assert isinstance(kind, (str, tuple, list))
        assert isinstance(duration, str)
        assert config is None or isinstance(config, dict)
        vs_gen = GenerationVisualizer()
        vs_gen.import_data(self.dfmt_genmix)
        if config is not None:
            vs_gen.import_config(config)
        vs_gen.plot_renewable_share(date, kind, duration)
        return vs_gen

    def plot_duck_curve(self, date=DATE_RANGE_OF_INTEREST, config=None):
        date = handle_date(date)
        assert config is None or isinstance(config, dict)
        vs_gen = GenerationVisualizer()
        vs_gen.import_data(self.dfmt_genmix)
        if config is not None:
            vs_gen.import_config(config)
        vs_gen.plot_duck_curve(date)
        return vs_gen

    def plot_price_series(self, date=DATE_RANGE_OF_INTEREST, mark_big_event=False, config=None):
        date = handle_date(date)
        assert isinstance(mark_big_event, bool)
        assert config is None or isinstance(config, dict)
        vs_prc = PriceVisualizer()
        vs_prc.import_data(self.dfmt_price)
        vs_prc.import_big_event(self.big_event)
        if config is not None:
            vs_prc.import_config(config)
        vs_prc.plot_price_series(date, mark_big_event)
        return vs_prc

    def plot_price_distribution(self, date=DATE_RANGE_OF_INTEREST, config=None):
        date = handle_date(date)
        assert config is None or isinstance(config, dict)
        vs_prc = PriceVisualizer()
        vs_prc.import_data(self.dfmt_price)
        if config is not None:
            vs_prc.import_config(config)
        vs_prc.plot_price_distribution(date)
        return vs_prc

    def plot_weather_series(self, date=DATE_RANGE_OF_INTEREST, kind='tmpc', config=None):
        date = handle_date(date)
        assert kind in ('tmpc', 'relh', 'sped')
        assert config is None or isinstance(config, dict)
        vs_wea = WeatherVisualizer()
        vs_wea.import_data(self.dfmt_weather)
        if config is not None:
            vs_wea.import_config(config)
        vs_wea.plot_weather_series(date, kind)
        return vs_wea

    def plot_mobility_series(self, *args, **kwargs):
        print('Warning: No mobility data in city level.')

    def plot_covid_series(self, date=DATE_RANGE_OF_INTEREST, kind='new_confirm', config=None):
        date = handle_date(date)
        assert kind in ('accum_confirm', 'new_confirm', 'infect_rate', 'accum_death', 'new_death', 'fatal_rate')
        assert config is None or isinstance(config, dict)
        vs_cov = CovidVisualizer()
        vs_cov.import_data(self.dfmt_covid)
        if config is not None:
            vs_cov.import_config(config)
        vs_cov.plot_covid_series(date, kind)
        return vs_cov


class City(RTO):
    def _import_data(self):
        if self.source is not None:  # no mobility below
            self.dfmt_demand.import_from_source(self.source['demand'])
            self.dfmt_weather.import_from_source(self.source['weather'])
            dfmt_mob1 = DataFormatter().import_from_source(self.source['patterns'])
            dfmt_mob2 = DataFormatter().import_from_source(self.source['social_distancing'])
            self.dfmt_mobility = merge_by_date((dfmt_mob1, dfmt_mob2)).handle_outlier(nan='drop')
            self.dfmt_mobility = self.dfmt_mobility.select_by_column(list(MOBILITY_KEYWORD.values()))
            self.dfmt_mobility.data_column = \
                self.dfmt_mobility.data_column.map({val: kw for (kw, val) in MOBILITY_KEYWORD.items()})
            self.dfmt_covid.import_from_source(self.source['covid'])
            if self.name != 'la':
                self.dfmt_price.import_from_source(self.source['price'])
            else:
                print('Warning: Please note that NO PRICE data in Los Angeles. Related functions may not work.')
        return self

    def cal_genmix_baseline(self, *args, **kwargs):
        print('Warning: No genmix data in city level.')

    def eval_genmix_baseline(self, *args, **kwargs):
        print('Warning: No genmix data in city level.')

    def plot_genmix_baseline(self, *args, **kwargs):
        print('Warning: No genmix data in city level.')

    # ::::: MOBILITY BASELINES ::::: #
    @staticmethod
    def _check_mobility_baseline_inputs(date, method, kind, shift_year):
        date = handle_date(date)
        assert method in ('date-alignment', 'week-alignment')
        assert kind in MOBILITY_KEYWORD.keys()
        assert isinstance(shift_year, int)
        return date, method, kind, shift_year

    def _init_mobility_baseline(self, date, method, kind, shift_year):
        if method == 'date-alignment':
            bl_da = DateAlignmentBaseline()
            bl_da.import_data(self.dfmt_mobility.select_by_column(kind))
            bl_da.import_target_date(date)
            bl_da.cal_baseline(shift_year)
            bl_da.get_observation()
            return bl_da
        else:  # week-alignment
            bl_wa = WeekAlignmentBaseline()
            bl_wa.import_data(self.dfmt_mobility.select_by_column(kind))
            bl_wa.import_target_date(date)
            bl_wa.cal_baseline(shift_year)
            bl_wa.get_observation()
            return bl_wa

    def cal_mobility_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='date-alignment', kind='retail', shift_year=1):
        date, method, kind, shift_year = self._check_mobility_baseline_inputs(date, method, kind, shift_year)
        bl = self._init_mobility_baseline(date, method, kind, shift_year)
        return bl.baseline.data

    def eval_mobility_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='date-alignment', kind='retail', shift_year=1):
        date, method, kind, shift_year = self._check_mobility_baseline_inputs(date, method, kind, shift_year)
        bl = self._init_mobility_baseline(date, method, kind, shift_year)
        mape, smape, rmse = bl.evaluate()
        return mape, smape, rmse

    def plot_mobility_baseline(
            self, date=DATE_RANGE_OF_INTEREST, method='date-alignment', kind='retail', shift_year=1):
        date, method, kind, shift_year = self._check_mobility_baseline_inputs(date, method, kind, shift_year)
        bl = self._init_mobility_baseline(date, method, kind, shift_year)
        bl.plot()
        return bl

    # ::::: REGRESSION ANALYSIS ::::: #
    def test_price_correlation(self, date=DATE_RANGE_OF_INTEREST):  # regression: price ~ demand + tmpc
        date = handle_date(date)
        ols = OrdinaryLeastSquares()
        dmd = self.dfmt_demand.select_by_date(after=date[0], before=date[-1]).flatten()
        tmpc = self.dfmt_weather.select_by_date(after=date[0], before=date[-1]).select_by_kind('tmpc').flatten()
        ols.train_x = merge_by_date({'demand': dmd, 'tmpc': tmpc}).data  # no gas
        ols.train_y = self.dfmt_price.select_by_date(after=date[0], before=date[-1]).flatten().data
        ols.train()
        return ols

    # ::::: PLOTTERS ::::: #
    def plot_generation_mix(self, *args, **kwargs):
        print('Warning: No genmix data in city level.')

    def plot_renewable_share(self, *args, **kwargs):
        print('Warning: No genmix data in city level.')

    def plot_duck_curve(self, *args, **kwargs):
        print('Warning: No genmix data in city level.')

    def plot_mobility_series(self, date=DATE_RANGE_OF_INTEREST, kind='retail', config=None):
        date = handle_date(date)
        assert kind in MOBILITY_KEYWORD.keys()
        vs_mob = MobilityVisualizer()
        vs_mob.import_data(self.dfmt_mobility)
        if config is not None:
            vs_mob.import_config(config)
        vs_mob.plot_mobility_series(date, kind)
        return vs_mob




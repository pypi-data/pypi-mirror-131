import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from scipy.stats import wasserstein_distance as wdist
from .data_structure import DataFormatter, import_data_in_group, merge_by_date, handle_date
from .visualizer import Visualizer
from .regressor import LearningRegressor, OrdinaryLeastSquares, AutoregressiveIntegratedMovingAverage

HIST_DATE_RANGE = pd.date_range('2017-01-01', '2019-12-31')
FIRST_CASE_DATE = pd.to_datetime('2020-01-20')


def shift_back_date(date, shift_year=1, shift_month=0, shift_day=0, output_type='start-end'):
    assert isinstance(date, pd.DatetimeIndex)
    assert isinstance(shift_year, int)  # forward: >0, backward: <0
    assert isinstance(shift_month, int)
    assert isinstance(shift_day, int)
    assert output_type in ('start-end', 'range')
    hist_date = pd.DataFrame({
        'year':  date.year - shift_year,
        'month': date.month - shift_month,
        'day':   date.day - shift_day,
    })
    hist_date = pd.to_datetime(hist_date, errors='coerce')  # get NaT for 2020-02-29 -> 2019-02-29 (not exist)
    if shift_year > 0 and np.any(hist_date > FIRST_CASE_DATE):
        print("Warning: Some baseline dates appear during the pandemic period. "
              "Please check if the shift back (default: 1 year) should be increased.")
    start, end = hist_date[hist_date.index[[0, -1]]]
    if output_type == 'start-end':
        return start, end
    else:  # range
        return hist_date


class BaselineEstimator(object):
    def __init__(self, name='baseline'):
        self.name = name
        self.observation = DataFormatter()
        self.baseline = DataFormatter()
        self.date = None

    def import_data(self, **kwargs):  # to specify
        return self

    def import_target_date(self, date):
        self.date = handle_date(date)
        return self

    def get_observation(self, **kwargs):  # to specify
        return self.observation

    def cal_baseline(self, **kwargs):  # to specify
        return self.baseline

    def evaluate(self, verbose=True, algo_type='stat-then-mean'):
        assert isinstance(verbose, bool)
        assert algo_type in ('stat-then-mean', 'mean-then-stat')
        assert len(self.observation) > 0 and len(self.baseline) > 0
        idx = [i for i in self.observation.data_index if i in self.baseline.data_index]
        obs = self.observation.select_by_index(idx).flatten().data_value
        est = self.baseline.select_by_index(idx).flatten().data_value
        if algo_type == 'mean-then-stat':
            obs, est = obs.mean(), est.mean()
        mape = np.abs(est / obs - 1).mean()
        smape = 2 * ((np.abs(obs - est)) / (np.abs(obs) + np.abs(est))).mean()
        rmse = np.sqrt(((obs - est) ** 2).mean())
        if verbose:
            print(f"Statistics of Difference from Baseline:\n"
                  f"[MAPE]  = {100*mape:.2f} %\n"
                  f"[sMAPE] = {100*smape:.2f} %\n"
                  f"[RMSE]  = {rmse:.2f}")
        return mape, smape, rmse

    def plot(self):
        assert len(self.observation) > 0 and len(self.baseline) > 0
        idx = [i for i in self.observation.data_index if i in self.baseline.data_index]
        obs = self.observation.select_by_index(idx).flatten()
        est = self.baseline.select_by_index(idx).flatten()
        idx = obs.data_index
        obs = obs.data_value
        est = est.data_value
        vs = Visualizer(name=self.name + '-visual').create_fig_ax(title='Baseline')
        plt.plot(idx, obs, label='Observation', c='k', lw=2)
        plt.plot(idx, est, label=f"Baseline [{self.name.title()}]", c='grey', lw=1.5, ls=':')
        if len(obs) > 200:
            vs.update_fig_ax(fig_width='full')
        vs.decorate_axis(ylabel='Comparison with Baseline', xrot=40, yrot=40)
        plt.legend()
        plt.show()


class DateAlignmentBaseline(BaselineEstimator):
    def __init__(self, name='date-alignment'):
        super().__init__(name)
        self.dfmt_x = DataFormatter()

    def import_data(self, source):
        assert isinstance(source, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source)
        return self

    def get_observation(self):
        assert len(self.dfmt_x) > 0
        assert self.date is not None
        self.observation = self.dfmt_x.select_by_date(after=self.date[0], before=self.date[-1])
        return self.observation

    def cal_baseline(self, shift_year=1):
        assert len(self.dfmt_x) > 0
        assert isinstance(shift_year, int) and shift_year > 0
        assert self.date is not None
        date1, date2 = shift_back_date(self.date, shift_year)
        self.baseline = self.dfmt_x.select_by_date(after=date1, before=date2)
        self.baseline.data_index = shift_back_date(self.baseline.data_index, -shift_year, output_type='range')
        return self.baseline


class WeekAlignmentBaseline(DateAlignmentBaseline):
    def __init__(self, name='week-alignment'):
        super().__init__(name)

    def cal_baseline(self, shift_year=1):
        def _shift_back_by_week_index(sr_day):
            year, week, weekday = sr_day.year, sr_day.week, sr_day.weekday
            all_dates = pd.date_range(str(year) + '-01-01', end=str(year) + '-12-31').isocalendar()
            select = all_dates[(all_dates.week == week) & (all_dates.day == weekday)].index
            if len(select) == 0:
                print('Warning: No aligned date is found!')
            return select.to_series().reset_index(drop=True)
        hist_day = pd.DataFrame({
            'year':    self.date.year - shift_year,
            'week':    self.date.isocalendar().week,
            'weekday': self.date.isocalendar().day,
        })
        hist_date = hist_day.apply(_shift_back_by_week_index, axis=1)[0]
        date1, date2 = hist_date[hist_date.index[[0, -1]]]
        self.baseline = self.dfmt_x.select_by_date(after=date1, before=date2)
        hist_day_ = pd.DataFrame({
            'year':    self.baseline.data_index.year + shift_year,
            'week':    self.baseline.data_index.isocalendar().week,
            'weekday': self.baseline.data_index.isocalendar().day,
        })
        hist_day_ = hist_day_.apply(_shift_back_by_week_index, axis=1)[0]
        self.baseline.data_index = hist_day_
        return self.baseline


class MonthAlignmentBaseline(DateAlignmentBaseline):
    def __init__(self, name='month-alignment'):
        super().__init__(name)

    def import_data(self, source):
        assert isinstance(source, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source)
        self.dfmt_x = self.dfmt_x.aggregate_by_hour(func=np.sum).aggregate_by_date(duration='1M', func=np.mean)
        return self


class WeeklyTrendBaseline(BaselineEstimator):
    def __init__(self, name='weekly-trend'):
        super().__init__(name)
        self.dfmt_x = DataFormatter()
        self.dfmt_t = DataFormatter()

    def import_data(self, source):
        assert isinstance(source, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source)
        self.dfmt_t = self.dfmt_x.moving_average(window=7*24)  # update immediately
        return self

    def get_observation(self):
        assert len(self.dfmt_t) > 0
        assert self.date is not None
        self.observation = self.dfmt_t.select_by_date(after=self.date[0], before=self.date[-1])
        return self.observation

    def cal_baseline(self, shift_year=1):
        assert len(self.dfmt_t) > 0
        assert isinstance(shift_year, int) and shift_year > 0
        assert self.date is not None
        date1, date2 = shift_back_date(self.date, shift_year)
        self.baseline = self.dfmt_t.select_by_date(after=date1, before=date2)
        self.baseline.data_index = shift_back_date(self.baseline.data_index, -shift_year, output_type='range')
        return self.baseline


class MonthlyTrendBaseline(BaselineEstimator, AutoregressiveIntegratedMovingAverage):
    def __init__(self, name='monthly-trend'):
        BaselineEstimator.__init__(self, name)
        AutoregressiveIntegratedMovingAverage.__init__(self, name)
        self.dfmt_x = DataFormatter()
        self.dfmt_t = DataFormatter()

    def import_data(self, source):
        assert isinstance(source, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source)
        self.dfmt_x = self.dfmt_x.aggregate_by_hour(func=np.sum).aggregate_by_date(duration='1M', func=np.mean)
        return self

    def update_trend_data(self, hist_date_range=HIST_DATE_RANGE, verbose=True):
        assert isinstance(hist_date_range, pd.DatetimeIndex)
        date1, date2 = hist_date_range[0], hist_date_range[-1]
        date2_ = date2 + pd.Timedelta('1D')
        self.train_x = self.dfmt_x.select_by_date(after=date1, before=date2).data
        n_step = len(pd.date_range(date2_, self.dfmt_x.data_index[-1], freq='1M'))  # freq is critical
        self.test_x = self.dfmt_x.select_by_date(after=date2_).data
        self.build_model(order=(2, 0, 1))  # fine-tuned p, d, q
        self.train(verbose)
        self.dfmt_t.import_from_dataframe(self.forecast(steps=n_step, extend=True))
        return self

    def get_observation(self):
        assert len(self.dfmt_x) > 0
        assert self.date is not None
        self.observation = self.dfmt_x.select_by_date(after=self.date[0], before=self.date[-1])
        return self.observation

    def cal_baseline(self):
        assert len(self.dfmt_t) > 0
        assert self.date is not None
        self.baseline = self.dfmt_t.select_by_date(after=self.date[0], before=self.date[-1])
        return self.baseline


class TempSensitiveTrendBaseline(BaselineEstimator, OrdinaryLeastSquares):
    def __init__(self, name='temperature-sensitive-trend'):
        BaselineEstimator.__init__(self, name)  # initialize manually
        OrdinaryLeastSquares.__init__(self, name)
        self.dfmt_x = DataFormatter()
        self.dfmt_tmpc = DataFormatter()
        self.dfmt_t = DataFormatter()

    def import_data(self, source_x, source_tmpc):
        assert isinstance(source_x, (str, tuple, pd.DataFrame, DataFormatter))
        assert isinstance(source_tmpc, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source_x)
        self.dfmt_tmpc = import_data_in_group(source_tmpc)
        return self

    def update_trend_data(self, hist_date_range=HIST_DATE_RANGE, verbose=True):
        assert isinstance(hist_date_range, pd.DatetimeIndex)
        tmpc = self.dfmt_tmpc.transform()
        tmpc_inputs = merge_by_date([tmpc, tmpc ** 2], column_name=['tmpc', 'tmpc2'])  # training inputs
        date1, date2 = hist_date_range[0], hist_date_range[-1]
        self.train_x = tmpc_inputs.select_by_date(after=date1, before=date2).data
        self.train_y = self.dfmt_x.transform().select_by_date(after=date1, before=date2).data
        self.train(verbose)
        pred = self.predict(tmpc_inputs.data)
        self.dfmt_t = self.dfmt_t.import_from_dataframe(pd.DataFrame(
            data=pred, index=self.dfmt_x.transform().data_index, columns=['trend']
        )).transform()
        return self

    def get_observation(self):
        assert len(self.dfmt_x) > 0
        assert self.date is not None
        self.observation = self.dfmt_x.select_by_date(after=self.date[0], before=self.date[-1])
        return self.observation

    def cal_baseline(self):
        assert len(self.dfmt_t) > 0
        assert self.date is not None
        self.baseline = self.dfmt_t.select_by_date(after=self.date[0], before=self.date[-1])
        return self.baseline


class BackcastBaseline(BaselineEstimator, LearningRegressor):
    def __init__(self, name='hourly-backcast'):
        BaselineEstimator.__init__(self, name)  # initialize manually
        LearningRegressor.__init__(self, name)
        self.dfmt_x = DataFormatter()
        self.dfmt_y = DataFormatter()
        self.dfmt_b = DataFormatter()

    def import_data(self, source_x, source_y):  # import dfmt_x/y
        assert isinstance(source_x, (str, tuple, dict, pd.DataFrame, pd.Series, DataFormatter))
        assert isinstance(source_y, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source_x)
        self.dfmt_y = import_data_in_group(source_y)
        return self

    def gen_train_test_data(self, hist_date_range=HIST_DATE_RANGE, frac_train=0.7, seed=121):
        # dfmt_x/y -> train/test_x/y, may need to specify
        assert isinstance(hist_date_range, pd.DatetimeIndex)
        date1, date2 = hist_date_range[0], hist_date_range[-1]
        sel_dfx = merge_by_date(self.dfmt_x).select_by_date(after=date1, before=date2).sample(frac=1, seed=seed).data
        sel_dfy = self.dfmt_y.select_by_date(after=date1, before=date2).sample(frac=1, seed=seed).data  # shuffle
        n_train = int(len(sel_dfx) * frac_train)
        self.train_x = sel_dfx.iloc[:n_train, :]
        self.test_x = sel_dfx.iloc[n_train:, :]
        self.train_y = sel_dfy.iloc[:n_train, :]
        self.test_y = sel_dfy.iloc[n_train:, :]
        return self  # above is the simplest logic, allow full extensions

    def build_model(self, **kwargs):  # to specify
        return self

    def update_backcast_data(self):  # model -> dfmt_b
        assert self.model is not None
        pred = self.predict(merge_by_date(self.dfmt_x).data)
        self.dfmt_b = self.dfmt_b.import_from_dataframe(pd.DataFrame(
            data=pred, index=self.train_y.index.append(self.test_y.index), columns=self.train_y.columns
        ))
        return self

    def get_observation(self):  # dfmt_y -> observation
        assert len(self.dfmt_y) > 0
        assert self.date is not None
        self.observation = self.dfmt_y.select_by_date(after=self.date[0], before=self.date[-1])
        return self.observation

    def cal_baseline(self):  # dfmt_b -> baseline
        assert len(self.dfmt_b) > 0
        assert self.date is not None
        self.baseline = self.dfmt_b.select_by_date(after=self.date[0], before=self.date[-1])
        return self.baseline


class BackcastDemandBaseline(BackcastBaseline):
    def __init__(self, name='hourly-backcast-demand'):
        super().__init__(name)
        self.dfmt_combine = DataFormatter()
        # In this case, dfmt_x = weather/calendar vars, dfmt_y = demand

    def import_data(self, source_x, source_y):
        super().import_data(source_x, source_y)  # for complex wide dataframe, split or not are both fine
        if isinstance(self.dfmt_x, dict):  # keep compatibility for dict
            dfmt_tmpc = self.dfmt_x['tmpc']
            dfmt_relh = self.dfmt_x['relh']
            dfmt_sped = self.dfmt_x['sped']
        elif isinstance(self.dfmt_x, DataFormatter) and self.dfmt_x.data_type == '(COMPLEX) WIDE DATAFRAME':
            dfmt_tmpc = self.dfmt_x.select_by_kind('tmpc')
            dfmt_relh = self.dfmt_x.select_by_kind('relh')
            dfmt_sped = self.dfmt_x.select_by_kind('sped')
        else:
            raise Exception('Error: dfmt_x is badly recognized!')
        dfmt_dmd = self.dfmt_y.flatten()
        dfmt_cald = dfmt_dmd.gen_calendar_data().select_by_column(['month', 'day', 'hour', 'weekday', 'holiday'])
        self.dfmt_combine = merge_by_date({
            ('month', 'day', 'hour', 'weekday', 'holiday'): dfmt_cald,
            'tmpc':     dfmt_tmpc.flatten(),
            'ave_tmpc': dfmt_tmpc.aggregate_by_hour(func=np.mean).expand(),
            'relh':     dfmt_relh.flatten(),
            'ave_relh': dfmt_relh.aggregate_by_hour(func=np.max).expand(),
            'sped':     dfmt_sped.flatten(),
            'demand':   dfmt_dmd,
        }, handle_duplicate='drop', handle_nan='drop')
        return self

    def gen_train_test_data(self, hist_date_range=HIST_DATE_RANGE, frac_train=0.7, seed=121):
        # dfmt_x/y -> train/test_x/y
        assert isinstance(hist_date_range, pd.DatetimeIndex)
        date1, date2 = hist_date_range[0], hist_date_range[-1]
        sel_dfmt_xy = self.dfmt_combine.select_by_date(after=date1, before=date2)
        sel_dfx = sel_dfmt_xy.select_by_column(exclude='demand').sample(frac=1, seed=seed).data
        sel_dfy = sel_dfmt_xy.select_by_column(include='demand').sample(frac=1, seed=seed).data
        n_train = int(len(sel_dfx) * frac_train)
        self.train_x = sel_dfx.iloc[:n_train, :]
        self.test_x = sel_dfx.iloc[n_train:, :]
        self.train_y = sel_dfy.iloc[:n_train, :]
        self.test_y = sel_dfy.iloc[n_train:, :]
        return self

    def build_model(self, n_hidden, seed=121):
        self.model = MLPRegressor(
            hidden_layer_sizes=n_hidden,
            activation='relu',
            learning_rate='adaptive',
            batch_size=512,
            max_iter=10000,
            alpha=0.001,
            early_stopping=True,
            random_state=seed,
        )
        return self

    def update_backcast_data(self):  # model -> dfmt_b
        assert self.model is not None
        allx = self.dfmt_combine.select_by_column(exclude='demand').data
        pred = self.predict(allx)
        self.dfmt_b = self.dfmt_b.import_from_dataframe(pd.DataFrame(data=pred, index=allx.index, columns=['demand']))
        self.dfmt_b = self.dfmt_b.lift()  # keep indices to show dates
        return self


class DistributionIndexBaseline(BaselineEstimator):
    def __init__(self, name='distribution-index'):
        super().__init__(name)
        self.dfmt_x = DataFormatter()
        self.dfmt_i = DataFormatter()

    def import_data(self, source):
        assert isinstance(source, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source)
        return self

    def update_fluc_index_data(self, hist_date_range=HIST_DATE_RANGE):
        assert isinstance(hist_date_range, pd.DatetimeIndex)
        print("Start calculating the fluctuation index. Might be a bit slow...")
        df_rng = self.dfmt_x.select_by_date(after=hist_date_range[0], before=hist_date_range[-1])
        monthly_distrib = {
            m: df_rng.select_by_year_month(month=m).data_value.flatten()
            for m in range(1, 12+1)
        }
        dfi = self.dfmt_x.data
        for idx in dfi.index:
            for col in dfi.columns:
                val = dfi.loc[idx, col]
                quantile = np.sum(monthly_distrib[idx.month] < val) / len(monthly_distrib[idx.month])
                dfi.loc[idx, col] = np.abs(2 * quantile - 1)
        self.dfmt_i.import_from_dataframe(dfi)
        print("Calculation is done.")
        return self

    def get_observation(self):
        assert len(self.dfmt_i) > 0
        assert self.date is not None
        self.observation = self.dfmt_i.select_by_date(after=self.date[0], before=self.date[-1])
        return self.observation

    def cal_baseline(self, shift_year=1):
        assert len(self.dfmt_i) > 0
        assert isinstance(shift_year, int) and shift_year > 0
        assert self.date is not None
        date1, date2 = shift_back_date(self.date, shift_year)
        self.baseline = self.dfmt_i.select_by_date(after=date1, before=date2)
        self.baseline.data_index = shift_back_date(self.baseline.data_index, -shift_year, output_type='range')
        return self.baseline

    def evaluate(self, verbose=True, algo_type='distrib-dist'):  # distributional distance by default
        assert algo_type in ('distrib-dist', 'stat-then-mean', 'mean-then-stat')
        if algo_type in ('stat-then-mean', 'mean-then-stat'):
            return super().evaluate(verbose, algo_type)
        else:  # distrib-dist
            assert isinstance(verbose, bool)
            assert len(self.observation) > 0 and len(self.baseline) > 0
            idx = [i for i in self.observation.data_index if i in self.baseline.data_index]
            obs = self.observation.select_by_index(idx).data_value.flatten()
            est = self.baseline.select_by_index(idx).data_value.flatten()
            dist = wdist(obs, est)
            if verbose:
                print(f"Statistics of Difference from Baseline:\n"
                      f"[Distrib-Dist] = {dist:.2f}")
            return dist


class DistributionDistanceBaseline(BaselineEstimator):
    def __init__(self, name='distribution-distance'):
        super().__init__(name)
        self.dfmt_x = DataFormatter()

    def import_data(self, source):
        assert isinstance(source, (str, tuple, pd.DataFrame, DataFormatter))
        self.dfmt_x = import_data_in_group(source)
        return self

    def get_observation(self):
        assert len(self.dfmt_x) > 0
        assert self.date is not None
        self.observation = self.dfmt_x.select_by_date(after=self.date[0], before=self.date[-1])
        return self.observation

    def cal_baseline(self, hist_date_range=HIST_DATE_RANGE):
        assert len(self.dfmt_x) > 0
        assert isinstance(hist_date_range, pd.DatetimeIndex)
        all_months = self.date.month.unique().values
        date_range = [d for d in hist_date_range if d.month in all_months]  # use data of same months
        date1, date2 = date_range[0], date_range[-1]
        self.baseline = self.dfmt_x.select_by_date(after=date1, before=date2)
        return self.baseline

    def evaluate(self, verbose=True, **kwargs):
        assert isinstance(verbose, bool)
        assert len(self.observation) > 0 and len(self.baseline) > 0
        idx = [i for i in self.observation.data_index if i in self.baseline.data_index]
        obs = self.observation.select_by_index(idx).data_value.flatten()
        est = self.baseline.select_by_index(idx).data_value.flatten()
        dist = wdist(obs, est)
        if verbose:
            print(f"Statistics of Difference from Baseline:\n"
                  f"[Distrib-Dist] = {dist:.2f}")
        return dist

    def plot(self):
        assert len(self.observation) > 0 and len(self.baseline) > 0
        obs = self.observation.transform().data_value
        est = self.baseline.transform().data_value
        ratio = (obs.max() - obs.min()) / (est.max() - est.min())
        vs = Visualizer(name=self.name + '-visual').create_fig_ax(title='Baseline')
        plt.hist(est, density=True, bins=100,
                 label=f"Baseline [{self.name.title()}]", color='grey', alpha=0.25)
        plt.hist(obs, density=True, bins=int(100*ratio),
                 label='Observation', color='k', alpha=0.5)  # distribution figures
        if len(obs) > 200:
            vs.update_fig_ax(fig_width='full')
        vs.decorate_axis(xlabel='Observations', ylabel='Probability Density', xrot=40, yrot=40)
        plt.legend()
        plt.show()


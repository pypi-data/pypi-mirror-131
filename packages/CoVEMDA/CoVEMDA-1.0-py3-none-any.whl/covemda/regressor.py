import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, pickle
from sklearn.preprocessing import MinMaxScaler
from statsmodels.api import OLS, add_constant
from statsmodels.tsa.api import VAR
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import durbin_watson


def handle_folder(folder):
    assert isinstance(folder, str)
    if not folder.endswith('/'):
        folder = folder + '/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def find_pickle_file(search_folder, file_name=None):
    search_folder = handle_folder(search_folder)
    assert file_name is None or (isinstance(file_name, str) and file_name.endswith('.pickle'))
    if file_name is None:
        outp = []
        for root, _, files in os.walk(search_folder):
            for file in files:
                if file.endswith('.pickle'):
                    outp.append(os.path.join(root, file))
        return outp  # return all .pickle files
    else:
        for root in ('../data/backcast/', 'data/backcast/', 'backcast/', './'):  # most likely
            if os.path.exists(root + file_name):
                return root + file_name
        for root, _, files in os.walk(search_folder):
            if file_name in files:
                return os.path.join(root, file_name)  # only return the first one
        return None  # return None when not found


class Regressor(object):
    def __init__(self, name='regressor'):
        self.name = name
        self.train_x, self.train_y = pd.DataFrame(None), pd.DataFrame(None)
        self.test_x, self.test_y = pd.DataFrame(None), pd.DataFrame(None)
        self.model = None

    def import_train_test_data(self, **kwargs):  # to specify
        return self

    def build_model(self, **kwargs):  # to specify
        self.model = None
        return self

    def save(self, folder='save/'):
        folder = handle_folder(folder)
        save_file = folder + self.name + '-' + pd.to_datetime('today').strftime('%Y%m%dT%H%M') + '.pickle'
        with open(save_file, 'wb') as fn:
            pickle.dump([self.name, self.model], fn)
        print(f"Model Saved: {save_file}")
        return self

    def load(self, pickle_file):
        assert isinstance(pickle_file, str)
        with open(pickle_file, 'rb') as fn:
            self.name, self.model = pickle.load(fn)
        return self

    def train(self, **kwargs):  # to specify
        return self

    def predict(self, pred_x=None):  # to specify
        pred_y = 0
        return pred_y

    def test(self):
        pred = np.array(self.predict(self.test_x)).flatten()
        real = np.array(self.test_y).flatten()
        rmse = np.sqrt(((real - pred) ** 2).mean())
        mape = np.abs(pred / real - 1).mean()
        print(f"\nTesting {self.__class__.__name__}:")
        print(f"RMSE = {rmse:.4f}, MAPE = {100*mape:.2f} %")
        return rmse, mape


class LearningRegressor(Regressor):  # machine learning regressors
    def __init__(self, name='learner'):
        super().__init__(name)
        self.processor_x = MinMaxScaler()
        self.processor_y = MinMaxScaler()

    def train(self, **kwargs):
        assert self.model is not None
        self.processor_x = self.processor_x.fit(self.train_x)
        train_xs = self.processor_x.transform(self.train_x)
        self.processor_y = self.processor_y.fit(self.train_y)
        train_ys = self.processor_y.transform(self.train_y).flatten()  # 1D
        self.model.fit(train_xs, train_ys, **kwargs)
        return self

    def predict(self, pred_x=None):
        assert self.model is not None
        if pred_x is None:
            pred_x = self.test_x
        pred_xs = self.processor_x.transform(pred_x)
        pred_ys = self.model.predict(pred_xs)
        pred_y = self.processor_y.inverse_transform(pred_ys[:, np.newaxis]).flatten()  # 1D
        return pred_y

    def save(self, folder='save/'):
        folder = handle_folder(folder)
        save_file = folder + self.name + '-' + pd.to_datetime('today').strftime('%Y%m%dT%H%M') + '.pickle'
        with open(save_file, 'wb') as fn:
            pickle.dump([self.name, self.model, self.processor_x, self.processor_y], fn)  # include processors
        print(f"Model Saved: {save_file}")
        return self

    def load(self, pickle_file):
        assert isinstance(pickle_file, str)
        with open(pickle_file, 'rb') as fn:
            self.name, self.model, self.processor_x, self.processor_y = pickle.load(fn)  # include processors
        return self


class OrdinaryLeastSquares(Regressor):
    def __init__(self, name='ols'):
        super().__init__(name)

    def train(self, verbose=True):
        assert isinstance(verbose, bool)
        if len(self.train_y.shape) >= 2:
            self.train_y = self.train_y[self.train_y.columns[0]]
        self.model = OLS(self.train_y, add_constant(self.train_x)).fit()
        if verbose:
            print(self.model.summary())
        return self

    def predict(self, pred_x=None):
        assert self.model is not None
        if pred_x is None:
            pred_x = self.test_x
        pred_y = self.model.predict(add_constant(pred_x))
        return pred_y

    def cal_correlation_coeff(self):
        if len(self.train_y.shape) >= 2:
            self.train_y = self.train_y[self.train_y.columns[0]]
        if len(self.test_y.shape) >= 2:
            self.test_y = self.test_y[self.test_y.columns[0]]
        all_train = pd.concat([self.train_x, self.train_y], axis=1)
        all_test = pd.concat([self.test_x, self.test_y], axis=1)
        corr1, corr2 = all_train.corr(), all_test.corr()
        if len(self.train_y) > 0:
            print(f"\nTrain Data Correlation:\n{corr1}")
        if len(self.test_y) > 0:
            print(f"\nTest Data Correlation:\n{corr2}")
        return corr1, corr2


class VectorAutoregression(Regressor):
    def __init__(self, name='var'):
        super().__init__(name)

    def train(self, verbose=True):
        assert isinstance(verbose, bool)
        if len(self.train_y.shape) >= 2:
            self.train_y = self.train_y[self.train_y.columns[0]]
        self.model = VAR(pd.concat([self.train_x, self.train_y], axis=1)).fit()
        if verbose:
            print(self.model.summary())
        return self

    def predict(self, pred_x=None):
        assert self.model is not None
        if pred_x is None:
            pred_x = self.test_x
        if len(self.test_y.shape) >= 2:
            self.test_y = self.test_y[self.test_y.columns[0]]
        inp = pd.concat([pred_x, self.test_y], axis=1).dropna()
        order = self.model.k_ar
        pred_y = self.model.forecast(y=inp.values[:order], steps=len(inp) - order)[:, -1]
        outp = np.hstack([self.test_y.values[:order], pred_y])  # supplement the head part
        return outp

    def model_verification(self):
        assert self.model is not None
        print(f"[Stability] Stable = {self.model.is_stable()}")
        order = self.model.k_ar
        lb_test = [
            acorr_ljungbox(self.model.resid[col], lags=order, return_df=False)[1][0]
            for col in self.model.resid
        ]
        print(f"[LB Test] P-Value = {lb_test}")
        dw_test = durbin_watson(self.model.resid)
        print(f"[DW Test] Statistics = {dw_test}")

    def impulse_response(self, periods=30):
        assert self.model is not None
        assert isinstance(periods, int) and periods > 0
        self.model.irf(periods=periods).plot_cum_effects(orth=False)
        plt.show()

    def variance_decomposition(self, periods=30):
        assert self.model is not None
        assert isinstance(periods, int) and periods > 0
        self.model.fevd(periods=periods).plot()
        plt.show()


class DataPrecheck(object):
    def __init__(self):
        self.df_raw = pd.DataFrame(None)
        self.df_data1 = pd.DataFrame(None)
        self.df_data2 = pd.DataFrame(None)
        self.lag = 1

    def update_data(self, **kwargs):  # to specify
        pass

    def test_stability(self):
        assert len(self.df_data2) > 0
        for name in self.df_data2.columns:
            test = self.df_data2[name].dropna().values
            adf = adfuller(test)
            print(f"[ADF Test] {name:15s}: Statistics = {adf[0]:5.3f}, P-Value = {adf[1]:.4f}")

    def test_cointegration(self):
        assert len(self.df_data1) > 0
        test = pd.DataFrame(self.df_data1).dropna()
        coint = coint_johansen(test, det_order=-1, k_ar_diff=self.lag)
        trace = coint.lr1[0]
        cvt = coint.cvt[0, 0]  # for 0.90
        print(f"[Cointegreation] Statistics = {trace:6.3f}, CV(90) = {cvt:6.3f}, "
              f"No Cointegration is Found = {trace > cvt}")

    def cal_grangers_causation_matrix(self):
        assert len(self.df_data2) > 0
        variables = self.df_data2.columns
        df = pd.DataFrame(
            np.zeros((len(variables), len(variables))),
            columns=[var + '_x' for var in variables],
            index=[var + '_y' for var in variables]
        )
        for c in df.columns:
            for r in df.index:
                test_result = grangercausalitytests(self.df_data2[[r, c]], maxlag=self.lag, verbose=False)
                p_values = [test_result[i + 1][0]['ssr_chi2test'][1] for i in range(self.lag)]
                min_p_value = np.min(p_values)
                df.loc[r, c] = min_p_value
        pd.set_option('display.max_columns', None)
        print(df)


class AutoregressiveIntegratedMovingAverage(Regressor):
    def __init__(self, name='arima'):
        super().__init__(name)
        self.order = (0, 0, 0)

    def build_model(self, order):
        self.order = order
        return self

    def train(self, verbose=True):
        assert isinstance(verbose, bool)
        self.model = ARIMA(self.train_x, order=self.order).fit()
        if verbose:
            print(self.model.summary())
        return self

    def forecast(self, steps=None, extend=False):  # special
        assert self.model is not None
        if steps is None:
            steps = len(self.test_x)
        pred1 = self.model.predict()
        pred2 = self.model.forecast(steps=steps)
        if extend:
            return pred1.append(pred2)
        else:
            return pred2

    def test(self):  # special
        pred = np.array(self.model.predict()).flatten()
        real = np.array(self.train_x).flatten()
        rmse = np.sqrt(((real - pred) ** 2).mean())
        mape = np.abs(pred / real - 1).mean()
        print(f"RMSE = {rmse:.4f}, MAPE = {100 * mape:.2f} %")
        return rmse, mape



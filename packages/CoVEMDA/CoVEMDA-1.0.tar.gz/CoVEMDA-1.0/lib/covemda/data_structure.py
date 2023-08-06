import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
import re

N_HOUR = 24
COL_HOUR = [f"{i:02d}:00" for i in range(24)]


def handle_date(date):
    assert isinstance(date, (str, pd.Timestamp, pd.DatetimeIndex))  # str, single date, or date range
    if isinstance(date, (str, pd.Timestamp)):
        date = pd.date_range(start=date, end=date)
    return date


class DataFormatter(object):
    def __init__(self, name=None):
        self.data = pd.DataFrame(None)
        self._data_name = name

    def copy(self):
        return DataFormatter(self.data_name).import_from_dataframe(df=self.data)

    @property
    def data_type(self):
        cols = set(self.data.columns)
        if cols == set(COL_HOUR):
            return '(SIMPLE) WIDE DATAFRAME'
        elif cols > set(COL_HOUR) and len(cols) == N_HOUR + 1:
            return '(COMPLEX) WIDE DATAFRAME'
        elif self.data.index.unique().inferred_freq == 'H':  # strict rule
            return 'LONG DATAFRAME'
        else:
            if isinstance(self.data.index, pd.DatetimeIndex):
                extend = self.data.resample('H').fillna(method='ffill')
                if len(self.data) >= 0.95 * len(extend):  # less than 5% missing data
                    return 'LONG DATAFRAME'
            return 'OTHER'

    @property
    def data_name(self):
        return self._data_name

    @data_name.setter
    def data_name(self, name):
        self._data_name = name
        if len(self.data.columns) == 1:  # series data
            self.data.columns = [name]

    @property
    def data_column(self):
        return self.data.columns

    @data_column.setter
    def data_column(self, cols):
        assert len(cols) == len(self.data.columns)
        self.data.columns = cols

    @property
    def data_index(self):
        return self.data.index

    @data_index.setter
    def data_index(self, index):
        assert len(index) == len(self.data.index)
        self.data.index = index

    @property
    def data_value(self):
        return self.data.values

    @data_value.setter
    def data_value(self, value):
        value = np.array(value)
        assert value.shape == self.data.shape
        for i in range(len(self.data.columns)):  # column-wise value setting
            self.data[self.data.columns[i]] = value[:, i]

    @property
    def col_kind(self):
        col = [c for c in self.data.columns if c not in COL_HOUR]
        return col[0] if len(col) > 0 else None

    @property
    def all_kinds(self):
        if self.data_type == '(COMPLEX) WIDE DATAFRAME':
            return self.data[self.col_kind].unique()
        elif self.data_type == 'LONG DATAFRAME':
            return self.data_column.unique()
        else:  # simple wide dataframe or other
            return None

    def __str__(self):
        return f"{self.data_name} ({self.data_type})"

    def __len__(self):
        return len(self.data)

    def __neg__(self):
        return DataFormatter(self.data_name).import_from_dataframe(df=-self.data)

    def __abs__(self):
        return DataFormatter(self.data_name).import_from_dataframe(df=self.data.abs())

    @staticmethod
    def _decorate_arg(other, cols):
        if isinstance(other, np.ndarray):
            return other if len(np.shape(other)) > 1 else other[:, np.newaxis]
        elif isinstance(other, pd.Series):
            return other.to_frame()
        elif isinstance(other, (DataFormatter, pd.DataFrame)):
            df_other = other.data if isinstance(other, DataFormatter) else other
            assert len(cols) == len(df_other.columns)
            if set(cols) != set(df_other.columns):
                df_other.columns = cols  # unify the columns
            return df_other
        else:
            return other

    def __add__(self, other):
        return DataFormatter(self.data_name).import_from_dataframe(
            df=self.data + self._decorate_arg(other, self.data_column)
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return DataFormatter(self.data_name).import_from_dataframe(
            df=self.data - self._decorate_arg(other, self.data_column)
        )

    def __rsub__(self, other):
        return self.__neg__().__add__(other)

    def __mul__(self, other):
        return DataFormatter(self.data_name).import_from_dataframe(
            df=self.data * self._decorate_arg(other, self.data_column)
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return DataFormatter(self.data_name).import_from_dataframe(
            df=self.data / self._decorate_arg(other, self.data_column)
        )

    def __rtruediv__(self, other):
        return self.__pow__(-1).__mul__(other)

    def __pow__(self, power):
        return DataFormatter(self.data_name).import_from_dataframe(df=self.data ** power)

    def import_from_web(self, web):
        assert web.startswith(('http://', 'https://', 'www.'))
        try:
            self.data = pd.read_csv(web, index_col='date')
            self.data_index = pd.to_datetime(self.data_index)
            if self.data_name is None:
                kws = re.findall(r"[_]([a-zA-Z0-9]+)[.][csv|xls|xlsx|txt]", web)
                if len(kws) > 0:
                    self.data_name = kws[-1]
            return self
        except:
            print('Error happens when connecting the web.')

    def import_from_file(self, file):
        assert file.endswith(('.csv', '.xlsx', '.xls', '.txt'))
        if file.endswith('.csv'):
            self.data = pd.read_csv(file, index_col='date')
        elif file.endswith('.xlsx') or file.endswith('.xls'):
            self.data = pd.read_excel(file, index_col='date')
        elif file.endswith('.txt'):
            self.data = pd.read_table(file, index_col='date')
        self.data_index = pd.to_datetime(self.data_index)
        if self.data_name is None:
            kws = re.findall(r"[_]([a-zA-Z0-9]+)[.][csv|xls|xlsx|txt]", file)
            if len(kws) > 0:
                self.data_name = kws[-1]
        return self

    def import_from_dataframe(self, df):
        assert isinstance(df, (pd.DataFrame, pd.Series))
        self.data = df if isinstance(df, pd.DataFrame) else df.to_frame()
        if isinstance(df, pd.DataFrame) and 'date' in df.columns:
            self.data = self.data.set_index('date')
        self.data_index = pd.to_datetime(self.data_index)
        if self.data_name is None and isinstance(df, pd.Series):
            self.data_name = df.name
        return self

    def import_from_source(self, source):  # top-level function to allow web, file, or dataframe
        if isinstance(source, str) and source.startswith(('http://', 'https://', 'www.')):
            return self.import_from_web(source)
        elif isinstance(source, str) and source.endswith(('.csv', '.xlsx', '.xls', '.txt')):
            return self.import_from_file(source)
        elif isinstance(source, (pd.DataFrame, pd.Series)):
            return self.import_from_dataframe(source)
        elif isinstance(source, DataFormatter):
            self.__dict__ = source.__dict__.copy()
            return self
        else:
            raise Exception('Unrecognized import source!')

    def select_by_date(self, after=None, before=None):  # get [after, before]
        assert after is None or isinstance(after, (str, pd.Timestamp))
        assert before is None or isinstance(before, (str, pd.Timestamp))
        df = self.copy().data
        if after is not None:
            df = df[df.index >= pd.to_datetime(after)]
        if before is not None:
            df = df[df.index <= pd.to_datetime(before)]
        dfmt_select = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_select

    def select_by_year_month(self, year=None, month=None):
        assert year is None or isinstance(year, int)
        assert month is None or (isinstance(month, int) and 1 <= month <= 12)
        df = self.copy().data
        if year is not None:
            df = df[df.index.year == year]
        if month is not None:
            df = df[df.index.month == month]
        dfmt_select = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_select

    def select_by_index(self, include=None, exclude=None):  # should specify all indices
        assert include is None or isinstance(include, (str, list, tuple))
        assert exclude is None or isinstance(exclude, (str, list, tuple))
        idx_inc, idx_exc = self.data_index, []
        if include is not None:
            idx_inc = [include] if isinstance(include, str) else list(include)
        if exclude is not None:
            idx_exc = [exclude] if isinstance(exclude, str) else list(exclude)
        idx_select = [i for i in self.data_index if i in idx_inc]
        idx_select = [i for i in idx_select if i not in idx_exc]
        df = self.data.loc[idx_select, :]
        dfmt_select = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_select

    def select_by_column(self, include=None, exclude=None):
        assert include is None or isinstance(include, (str, list, tuple))
        assert exclude is None or isinstance(exclude, (str, list, tuple))
        col_inc, col_exc = self.data_column, []
        if include is not None:
            col_inc = [include] if isinstance(include, str) else list(include)
        if exclude is not None:
            col_exc = [exclude] if isinstance(exclude, str) else list(exclude)
        col_select = [c for c in self.data_column if c in col_inc]
        col_select = [c for c in col_select if c not in col_exc]
        df = self.data[col_select]
        if len(col_select) == 1:  # series data
            dfmt_select = DataFormatter(col_select[0]).import_from_dataframe(df)
        else:
            dfmt_select = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_select

    def select_by_kind(self, kind):  # complex -> simple wide dataframe / long -> long dataframe
        assert self.data_type == '(COMPLEX) WIDE DATAFRAME' \
               or (self.data_type == 'LONG DATAFRAME' and len(self.data_column) > 1)
        assert isinstance(kind, (str, list, tuple))
        if self.data_type == '(COMPLEX) WIDE DATAFRAME':
            col_kind = self.col_kind
            if isinstance(kind, str):
                df = self.data[self.data[col_kind] == kind].drop(columns=col_kind)
                name = kind
            elif len(kind) == 1:  # equivalent to str case
                df = self.data[self.data[col_kind] == kind[0]].drop(columns=kind[0])
                name = kind[0]
            else:  # list or tuple
                df = self.data[self.data[col_kind].isin(kind)]
                name = self.data_name
        else:  # long dataframe
            sel_kind = [kind] if isinstance(kind, str) else kind
            df = self.data[self.data.columns[self.data_column.isin(sel_kind)]]
            name = self.data_name
        return DataFormatter(name).import_from_dataframe(df)

    def transform(self):  # long <-> wide dataframe
        if self.data_type in ('(SIMPLE) WIDE DATAFRAME', '(COMPLEX) WIDE DATAFRAME'):
            return self.flatten()
        elif self.data_type == 'LONG DATAFRAME':
            return self.lift()
        else:  # OTHER
            print('Warning: No changes when transforming the OTHER type!')
            return self

    def flatten(self):  # wide -> long dataframe
        if self.data_type == '(SIMPLE) WIDE DATAFRAME':
            df = self.data.copy()
            df.index = df.index.astype(str)
            sr = df.stack()
            sr.index = pd.to_datetime(sr.index.map('T'.join))
            dfmt_trans = DataFormatter(self.data_name).import_from_dataframe(sr.to_frame(self.data_name))
            return dfmt_trans
        elif self.data_type == '(COMPLEX) WIDE DATAFRAME':
            col_kind = self.col_kind
            all_kinds = self.all_kinds
            df = pd.concat([self.select_by_kind(kd).transform().data for kd in all_kinds], axis=1)
            df.columns = all_kinds
            df.columns.name = col_kind
            dfmt_trans = DataFormatter(self.data_name).import_from_dataframe(df)
            return dfmt_trans
        else:  # LONG DATAFRAME or OTHER
            return self

    def lift(self):  # long -> wide dataframe
        if self.data_type == 'LONG DATAFRAME':
            if len(self.data_column) == 1:
                sr = self.data[self.data_column[0]]
                sr.index = [sr.index.normalize(), sr.index.strftime('%H:%M')]
                dfmt_trans = DataFormatter().import_from_dataframe(sr.unstack())
                return dfmt_trans
            else:
                list_kind = self.data_column
                dfs = []
                for kd in list_kind:
                    tmp = self.select_by_column(include=kd).transform().data
                    cname = self.data.columns.name
                    col_kind = cname if cname is not None else 'kind'
                    tmp.insert(loc=0, column=col_kind, value=kd)  # add a column
                    dfs.append(tmp)
                df = pd.concat(dfs, axis=0).sort_index()
                dfmt_trans = DataFormatter(self.data_name).import_from_dataframe(df)
                return dfmt_trans
        else:  # WIDE DATAFRAME or OTHER
            return self

    def shift_back(self, step):  # e.g. step='1W'/'2D'/'12H'
        assert isinstance(step, str)
        df = self.data.copy()
        df.index = df.index + pd.to_timedelta(step)
        dfmt_shift = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_shift

    def moving_average(self, window, center=True):
        assert isinstance(window, int) and isinstance(center, bool)
        assert self.data_type != 'OTHER'
        df = self.data if self.data_type == 'LONG DATAFRAME' else self.transform().data
        df = df.rolling(window=window, center=center).mean()
        dfmt = DataFormatter(self.data_name).import_from_dataframe(df)
        dfmt = dfmt.handle_outlier(nan='drop') if self.data_type == 'LONG DATAFRAME' \
            else dfmt.transform().handle_outlier(nan='drop')
        return dfmt

    def sample(self, n=None, frac=None, seed=None):
        assert n is None or isinstance(n, int)
        assert frac is None or (isinstance(frac, (float, int)) and 0 <= frac <= 1)
        assert seed is None or isinstance(seed, int)
        assert n is not None or frac is not None
        df = self.data.copy()
        if n is not None:
            df = df.sample(n=n, random_state=seed) if seed is not None else df.sample(n=n)
        elif frac is not None:
            df = df.sample(frac=frac, random_state=seed) if seed is not None else df.sample(frac=frac)
        df = df.sort_index()
        dfmt_shuffle = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_shuffle

    def handle_outlier(self, duplicate=None, nan=None):
        assert duplicate in (None, 'drop')
        assert duplicate is not None or nan is not None
        df = self.data.copy()
        if duplicate == 'drop':
            df = self.data.drop_duplicates()
        if nan == 'drop':
            df = self.data.dropna()
        elif nan in ('backfill', 'bfill', 'pad', 'ffill'):
            df = self.data.fillna(method=nan)
        elif nan is not None:
            df = self.data.fillna(value=nan)
        dfmt_hand = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_hand

    def gen_calendar_data(self):
        holidays = USFederalHolidayCalendar().holidays()  # for US
        if self.data_type == '(SIMPLE) WIDE DATAFRAME' or self.data_type == '(COMPLEX) WIDE DATAFRAME':
            df = pd.DataFrame({
                'month':   self.data_index.month,
                'day':     self.data_index.day,
                'weekday': self.data_index.weekday,
                'holiday': (self.data_index.isin(holidays)).astype(int),
            }, index=self.data_index)
            dfmt_cal = DataFormatter('calendar').import_from_dataframe(df)
            return dfmt_cal
        elif self.data_type == 'LONG DATAFRAME':
            df = pd.DataFrame({
                'month':   self.data_index.month,
                'day':     self.data_index.day,
                'hour':    self.data_index.hour,
                'weekday': self.data_index.weekday,
                'holiday': (self.data_index.normalize().isin(holidays)).astype(int),
            }, index=self.data_index)
            dfmt_cal = DataFormatter('calendar').import_from_dataframe(df)
            return dfmt_cal
        else:
            raise Exception('Cannot generate calendar data from OTHER type!')

    def expand(self, fill='ffill'):  # daily -> hourly data
        assert self.data_index.unique().inferred_freq == 'D'
        assert fill in ('backfill', 'bfill', 'pad', 'ffill')
        if self.data_type != 'OTHER':
            raise Exception('Only OTHER type is supported for expansion!')
        df = self.data.resample('1H').fillna(fill)
        dfmt_expand = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_expand

    def aggregate_by_hour(self, func=np.sum):  # shrink columns to one, e.g. func=np.max
        assert callable(func)
        df = self.data.apply(func, axis=1).to_frame(self.data_name)
        dfmt_shrink = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_shrink

    def aggregate_by_date(self, duration='1M', func=np.mean):  # shrink rows, e.g. duration='1M'/'7D', func=np.mean
        assert isinstance(duration, str)
        assert callable(func)
        if self.data_type != '(COMPLEX) WIDE DATAFRAME':
            df = self.data.resample(duration).agg(func, axis=0)
        else:  # complex wide dataframe
            df = self.data.groupby([pd.Grouper(freq=duration), self.col_kind]).agg(func, axis=0)
            df = df.reset_index(level=1)
            # df = self.data.groupby(self.col_kind).resample(duration).apply(func, axis=0)
        dfmt_shrink = DataFormatter(self.data_name).import_from_dataframe(df)
        return dfmt_shrink

    def aggregate_by_kind(self, kind=None, func=np.sum):  # shrink kind col
        if self.data_type != '(COMPLEX) WIDE DATAFRAME':
            raise Exception('Only (COMPLEX) WIDE DATAFRAME type is supported aggregation by kind!')
        assert kind is None or isinstance(kind, (str, tuple, list))
        if isinstance(kind, str):
            return self.select_by_kind(kind)
        else:
            df = self.data if kind is None else self.select_by_kind(kind).data
            df = df.groupby(by=df.index).agg(func, axis=0)
            if self.col_kind in df.columns:
                df = df.drop(columns=self.col_kind)
            dfmt_shrink = DataFormatter(self.data_name).import_from_dataframe(df)
            return dfmt_shrink


def merge_by_date(dfmts, column_name=None, handle_duplicate=None, handle_nan=None):  # date aligned, like hstack
    assert isinstance(dfmts, (list, tuple, dict))
    assert column_name is None or len(column_name) == np.sum([len(dfmt.data_column) for dfmt in dfmts])
    assert handle_duplicate is None or isinstance(handle_duplicate, str)
    if isinstance(dfmts, (list, tuple)):
        assert np.all([isinstance(d, DataFormatter) for d in dfmts])
        df = pd.concat([d.data for d in dfmts], axis=1)
    else:  # dict
        assert np.all([isinstance(d, DataFormatter) for d in dfmts.values()])
        df = pd.concat([d.data for d in dfmts.values()], axis=1)
        cols = []
        for c in dfmts.keys():
            if isinstance(c, (list, tuple)):
                cols += list(c)  # concat
            else:
                cols += [c]
        df.columns = cols
    if column_name is not None:
        df.columns = column_name
    dfmt_merge = DataFormatter('merge').import_from_dataframe(df)
    if handle_duplicate is not None or handle_nan is not None:
        dfmt_merge = dfmt_merge.handle_outlier(handle_duplicate, handle_nan)
    return dfmt_merge


def merge_by_column(dfmts, column_name=None, handle_duplicate=None, handle_nan=None):  # column aligned, like vstack
    assert isinstance(dfmts, (tuple, list)) and np.all([isinstance(d, DataFormatter) for d in dfmts])
    assert column_name is None or len(column_name) == len(dfmts[0].data_column)
    assert handle_duplicate is None or isinstance(handle_duplicate, str)
    df = pd.concat([d.data for d in dfmts], axis=0)
    if column_name is not None:
        df.columns = column_name
    dfmt_merge = DataFormatter('merge').import_from_dataframe(df)
    if handle_duplicate is not None or handle_nan is not None:
        dfmt_merge = dfmt_merge.handle_outlier(handle_duplicate, handle_nan)
    return dfmt_merge


def import_data_in_group(source):  # build group(dict) of DataFormatter
    assert isinstance(source, (str, tuple, pd.DataFrame, DataFormatter, dict))
    if isinstance(source, str):
        return import_data_in_group((source, None))
    elif isinstance(source, tuple):
        assert len(source) == 2
        src, kind = source
        outp = DataFormatter().import_from_source(src)
        if kind is not None:
            outp = outp.select_by_kind(kind)
        return outp
    elif isinstance(source, pd.DataFrame):
        return DataFormatter().import_from_source(source)
    elif isinstance(source, DataFormatter):
        return source.copy()
    else:  # dict type
        info = pd.DataFrame(source, index=['source', 'kind']).T
        all_src = info['source'].unique()
        all_raw_dfmt = {src: import_data_in_group((src, None)) for src in all_src}
        outp = {}
        for kw, src, kind in info.itertuples():
            outp[kw] = all_raw_dfmt[src]
            if kind is not None:
                outp[kw] = outp[kw].select_by_kind(kind)
        return outp




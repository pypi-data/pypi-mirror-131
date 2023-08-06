import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .data_structure import DataFormatter, handle_date

plt.rcParams['pdf.fonttype'] = 42  # editable fonts
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['legend.frameon'] = False  # no legend frame


class Visualizer(object):
    def __init__(self, name='visual'):
        self.name = name
        self.figs, self.axs = [], []

    def create_fig_ax(self, title):
        fig = plt.figure(title, figsize=(5, 5))  # default: half width
        ax = fig.add_axes((0.15, 0.15, 0.8, 0.8))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        self.figs.append(fig)
        self.axs.append(ax)
        return self

    def update_fig_ax(self, index=-1, fig_width=None, ax_rect=None):
        assert fig_width in (None, 'half', 'full')  # half means 2-col figure
        assert ax_rect is None or (isinstance(ax_rect, list) and len(ax_rect) == 4)
        assert fig_width is not None or ax_rect is not None
        if fig_width == 'half':
            self.figs[index].set_size_inches(5, 5)
            self.axs[index].set_position((0.15, 0.15, 0.8, 0.8) if ax_rect is None else ax_rect)
        elif fig_width == 'full':
            self.figs[index].set_size_inches(10, 5)
            self.axs[index].set_position((0.08, 0.15, 0.9, 0.8) if ax_rect is None else ax_rect)
        else:  # only update axis
            self.axs[index].rect = ax_rect

    @staticmethod
    def decorate_axis(xlabel=None, xticks=None, xlim=None, xrot=None,
                      ylabel=None, yticks=None, ylim=None, yrot=None):
        assert xlabel is None or isinstance(xlabel, str)
        assert ylabel is None or isinstance(ylabel, str)
        assert xticks is None or isinstance(xticks, dict)
        assert yticks is None or isinstance(yticks, dict)
        assert xlim is None or (isinstance(xlim, list) and len(xlim) == 2)
        assert ylim is None or (isinstance(ylim, list) and len(ylim) == 2)
        assert xrot is None or (isinstance(xrot, int) and 0 <= xrot <= 90)
        assert yrot is None or (isinstance(yrot, int) and 0 <= yrot <= 90)
        if xlabel is not None:
            plt.xlabel(xlabel)
        if ylabel is not None:
            plt.ylabel(ylabel)
        if xticks is not None:
            plt.xticks(list(xticks.keys()), xticks.values())
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        if xrot is not None:
            plt.xticks(rotation=45, ha='right', rotation_mode='anchor')
        if yrot is not None:
            plt.yticks(rotation=45, ha='right', rotation_mode='anchor')


class VisualizerPlus(Visualizer):  # with several more features
    def __init__(self, name='visual2'):
        super().__init__(name)
        self.dfmt_x = DataFormatter()
        self.big_event = {}
        self.config = {}

    def import_data(self, source):
        assert isinstance(source, (str, pd.DataFrame, pd.Series, DataFormatter))
        self.dfmt_x.import_from_source(source)
        return self  # support complex wide dataframe

    def import_big_event(self, dict_event):
        assert isinstance(dict_event, dict)
        try:
            self.big_event = {
                kw: pd.to_datetime(val)
                for (kw, val) in dict_event.items()
            }
        except:
            print('Error: Unrecognized formats for big events!')
        return self

    def import_config(self, dict_setting):
        assert set(dict_setting.keys()) <= set(self.config.keys())
        for kw, val in dict_setting.items():  # config when mentioned
            for valkw, valval in val.items():
                self.config[kw][valkw] = valval
        return self


class DemandVisualizer(VisualizerPlus):
    def __init__(self, name='visual_demand'):
        super().__init__(name)
        # In this class, self.dfmt_x = load data
        self.config = {
            'demand_series': dict(color='C0', linewidth=2),
            'demand_series_moving_average': dict(color='grey', linewidth=2, linestyle=':'),
            'demand_series_big_event': dict(color='m', linewidth=1.5, linestyle='--'),
            'demand_profile': dict(color='C0', linewidth=2),
            'demand_profile_interval1': dict(color='C0', alpha=0.25, linewidth=0),
            'demand_profile_interval2': dict(color='C0', alpha=0.1, linewidth=0),
        }

    def plot_demand_series(self, date, mark_big_event=False):
        assert isinstance(mark_big_event, bool)
        date = handle_date(date)
        dfmt_sel = self.dfmt_x.transform().select_by_date(after=date[0], before=date[-1])
        df_sel = dfmt_sel.data
        self.create_fig_ax(title='Demand Series')
        self.axs[-1].plot(
            df_sel.index, df_sel.values,
            label='Demand Series',
            **self.config['demand_series'],
        )
        if len(df_sel) > 7*24:
            df_ma = dfmt_sel.moving_average(window=7 * 24, center=True).data
            self.axs[-1].plot(
                df_ma.index, df_ma.values,
                label='Weekly Moving Average',
                **self.config['demand_series_moving_average'],
            )
        if mark_big_event:
            for kw, val in self.big_event.items():
                if val in date:
                    self.axs[-1].axvline(x=val, **self.config['demand_series_big_event'])
                    self.axs[-1].text(
                        x=val+pd.Timedelta('5h'), y=0.96*self.axs[-1].get_ylim()[1], s=kw.replace('_', ' '),
                        color=self.config['demand_series_big_event']['color'], rotation=10)
        if len(df_sel) > 200:
            self.update_fig_ax(fig_width='full')
        self.decorate_axis(ylabel='Demand Series [MW]', xrot=40, yrot=40)
        plt.legend()
        plt.show()

    def plot_daily_demand_profile(self, date):
        date = handle_date(date)
        dfmt_sel = self.dfmt_x.select_by_date(after=date[0], before=date[-1])
        df_sel = dfmt_sel.data
        df_q = df_sel.quantile([0.1, 0.25, 0.5, 0.75, 0.9])
        self.create_fig_ax(title='Daily Demand Profile')
        self.axs[-1].plot(
            df_q.columns, df_q.loc[0.5],
            label='Average',
            **self.config['demand_profile'],
        )
        self.axs[-1].fill_between(
            df_q.columns, df_q.loc[0.25], df_q.loc[0.75],
            label='25-75% Interval',
            **self.config['demand_profile_interval1'],
        )
        self.axs[-1].fill_between(
            df_q.columns, df_q.loc[0.1], df_q.loc[0.9],
            label='10-90% Interval',
            **self.config['demand_profile_interval2'],
        )
        xticks = {i: df_q.columns[i] for i in list(range(0, 24, 3)) + [23]}
        self.decorate_axis(ylabel='Daily Demand Profile [MW]', xticks=xticks, xrot=40, yrot=40)
        plt.legend()
        plt.show()


class GenerationVisualizer(VisualizerPlus):
    def __init__(self, name='visual_generation'):
        super().__init__(name)
        # In this class, self.dfmt_x = genmix data
        color_mapping = {
            'coal':    '#a67a6d',
            'gas':     '#f69850',
            'oil':     '#b35711',
            'nuclear': '#3f9b98',
            'hydro':   '#a0d8f1',
            'wind':    '#73c698',
            'solar':   '#ffbd4a',
            'other':   '#b4b4b4',
            'import':  'white',
        }
        self.config = {
            'generation_mix': dict(colormap=color_mapping),
            'renewable_share': dict(colormap=color_mapping, linewidth=2),
            'duck_curve': dict(color='C0', linewidth=2),
            'duck_curve_interval1': dict(color='C0', alpha=0.25, linewidth=0),
            'duck_curve_interval2': dict(color='C0', alpha=0.1, linewidth=0),
        }

    def plot_generation_mix(self, date, duration='1M'):
        assert isinstance(duration, str)
        date = handle_date(date)
        dfmt_sel = self.dfmt_x.select_by_date(after=date[0], before=date[-1])
        dfmt_sel = dfmt_sel.transform().aggregate_by_date(duration=duration, func=np.sum)
        df_sel = dfmt_sel.data
        self.create_fig_ax(title='Generation Mix')
        color_mapping = self.config['generation_mix']['colormap']
        all_kinds = [c for c in color_mapping if c in dfmt_sel.data_column]  # ordered list
        self.axs[-1].stackplot(
            df_sel.index, [100 * df_sel[k].values / df_sel.sum(axis=1) for k in all_kinds],
            labels=[k.title() + ' Energy' for k in all_kinds],
            colors=[color_mapping[k] for k in all_kinds],
        )
        if len(df_sel) > 200:
            self.update_fig_ax(fig_width='full')
        self.decorate_axis(ylabel='Generation Proportion [%]', xrot=40)
        plt.legend()
        plt.show()

    def plot_renewable_share(self, date, kind=('hydro', 'solar', 'wind'), duration='1M'):
        assert isinstance(kind, (str, tuple, list))
        assert isinstance(duration, str)
        date = handle_date(date)
        kind = (kind,) if isinstance(kind, str) else kind
        dfmt_sel = self.dfmt_x.select_by_date(after=date[0], before=date[-1]).transform()
        renewable_kind = [k for k in dfmt_sel.data_column if k in kind and k in ('hydro', 'solar', 'wind')]
        assert len(renewable_kind) > 0
        df_renewable = dfmt_sel.select_by_kind(renewable_kind).aggregate_by_date(duration=duration, func=np.sum).data
        df_allgen = dfmt_sel.aggregate_by_date(duration=duration, func=np.sum).data
        self.create_fig_ax(title='Renewable Share')
        color_mapping = self.config['renewable_share']['colormap']
        other_config = self.config['renewable_share'].copy()
        other_config.pop('colormap')
        for k in renewable_kind:
            self.axs[-1].plot(
                df_renewable.index, 100 * df_renewable[k].values / df_allgen.sum(axis=1),
                label=k.title() + ' Energy',
                color=color_mapping[k], **other_config,
            )
        if len(df_renewable) > 200:
            self.update_fig_ax(fig_width='full')
        self.decorate_axis(ylabel='Renewable Share [%]', xrot=40)
        plt.legend()
        plt.show()

    def plot_duck_curve(self, date):
        date = handle_date(date)
        dfmt_sel = self.dfmt_x.select_by_date(after=date[0], before=date[-1])
        dfmt_duck_curve = sum([dfmt_sel.select_by_kind(k) for k in dfmt_sel.all_kinds if k != 'solar'])
        df_duck_curve = dfmt_duck_curve.data
        df_q = df_duck_curve.quantile([0.1, 0.25, 0.5, 0.75, 0.9])
        self.create_fig_ax(title='Duck Curve')
        self.axs[-1].plot(
            df_q.columns, df_q.loc[0.5],
            label='Average',
            **self.config['duck_curve'],
        )
        self.axs[-1].fill_between(
            df_q.columns, df_q.loc[0.25], df_q.loc[0.75],
            label='25-75% Interval',
            **self.config['duck_curve_interval1'],
        )
        self.axs[-1].fill_between(
            df_q.columns, df_q.loc[0.1], df_q.loc[0.9],
            label='10-90% Interval',
            **self.config['duck_curve_interval2'],
        )
        if len(df_q) > 200:
            self.update_fig_ax(fig_width='full')
        xticks = {i: df_q.columns[i] for i in list(range(0, 24, 3)) + [23]}
        self.decorate_axis(ylabel='Duck Curve [MW]', xticks=xticks, xrot=40, yrot=40)
        plt.legend()
        plt.show()


class PriceVisualizer(VisualizerPlus):
    def __init__(self, name='visual_price'):
        super().__init__(name)
        # In this class, self.dfmt_x = price data
        self.config = {
            'price_series': dict(color='plum', linewidth=2),
            'price_series_moving_average': dict(color='grey', linewidth=2, linestyle=':'),
            'price_series_big_event': dict(color='m', linewidth=1.5, linestyle='--'),
            'price_distribution': dict(bins=50, color='plum'),
        }

    def plot_price_series(self, date, mark_big_event=False):
        assert isinstance(mark_big_event, bool)
        date = handle_date(date)
        dfmt_sel = self.dfmt_x.transform().select_by_date(after=date[0], before=date[-1])
        df_sel = dfmt_sel.data
        self.create_fig_ax(title='Price Series')
        self.axs[-1].plot(
            df_sel.index, df_sel.values,
            label='Price Series',
            **self.config['price_series'],
        )
        if len(df_sel) > 7*24:
            df_ma = dfmt_sel.moving_average(window=7 * 24, center=True).data
            self.axs[-1].plot(
                df_ma.index, df_ma.values,
                label='Weekly Moving Average',
                **self.config['price_series_moving_average'],
            )
        if mark_big_event:
            for kw, val in self.big_event.items():
                if val in date:
                    self.axs[-1].axvline(x=val, **self.config['price_series_big_event'])
                    self.axs[-1].text(
                        x=val+pd.Timedelta('5h'), y=0.96*self.axs[-1].get_ylim()[1], s=kw.replace('_', ' '),
                        color=self.config['price_series_big_event']['color'], rotation=10)
        if len(df_sel) > 200:
            self.update_fig_ax(fig_width='full')
        self.decorate_axis(ylabel='Price Series [USD/MWh]', xrot=40, yrot=40)
        plt.legend()
        plt.show()

    def plot_price_distribution(self, date):
        date = handle_date(date)
        dfmt_sel = self.dfmt_x.transform().select_by_date(after=date[0], before=date[-1])
        df_sel = dfmt_sel.data
        self.create_fig_ax(title='Price Distribution')
        self.axs[-1].hist(
            df_sel.values, density=True,
            label='Price Distribution',
            **self.config['price_distribution'],
        )
        self.decorate_axis(xlabel='Price [USD/MWh]', ylabel='Probability Density')
        plt.legend()
        plt.show()


class WeatherVisualizer(VisualizerPlus):
    def __init__(self, name='visual_weather'):
        super().__init__(name)
        # In this class, self.dfmt_x = weather data
        self.config = {
            'weather_series': dict(color='olive', linewidth=2),
            'weather_series_moving_average': dict(color='grey', linewidth=2, linestyle=':'),
        }

    def plot_weather_series(self, date, kind='tmpc'):
        date = handle_date(date)
        assert kind in ('tmpc', 'relh', 'sped')
        dfmt_sel = self.dfmt_x.select_by_date(after=date[0], before=date[-1])
        dfmt_sel = dfmt_sel.transform().select_by_kind(kind)
        df_sel = dfmt_sel.data
        self.create_fig_ax(title='Weather Series')
        self.axs[-1].plot(
            df_sel.index, df_sel.values,
            label=kind.title() + ' Observation',
            **self.config['weather_series'],
        )
        if len(df_sel) > 7*24:
            df_ma = dfmt_sel.moving_average(window=7 * 24, center=True).data
            self.axs[-1].plot(
                df_ma.index, df_ma.values,
                label='Weekly Moving Average',
                **self.config['weather_series_moving_average'],
            )
        if len(df_sel) > 200:
            self.update_fig_ax(fig_width='full')
        self.decorate_axis(ylabel='Weather Observation', xrot=40)
        plt.legend()
        plt.show()


class MobilityVisualizer(VisualizerPlus):
    def __init__(self, name='visual_mobility'):
        super().__init__(name)
        # In this class, self.dfmt_x = mobility data
        self.config = {
            'mobility_series': dict(color='sandybrown', linewidth=2),
            'mobility_series_big_event': dict(color='m', linewidth=1.5, linestyle='--'),
        }
        self.keywords = {
            'retail':          'Retail',
            'grocery':         'Grocery_Pharmacy',
            'restaurant':      'Restaurant_Recreaction',
            'completely_home': 'completely_home_device_count',
            'median_home':     'median_home_dwell_time',
            'part_time_work':  'part_time_work_behavior_devices',
            'full_time_work':  'full_time_work_behavior_devices',
        }

    def import_data(self, source):
        super().import_data(source)
        if list(self.keywords)[0] not in self.dfmt_x.data_column:  # simplify the column names
            self.dfmt_x.data_column = self.dfmt_x.data_column.map({val: kw for (kw, val) in self.keywords.items()})
        return self

    def plot_mobility_series(self, date, kind='retail', mark_big_event=False):
        date = handle_date(date)
        assert kind in self.keywords.keys()
        dfmt_sel = self.dfmt_x.select_by_date(after=date[0], before=date[-1])
        dfmt_sel = dfmt_sel.select_by_column(include=kind)
        df_sel = dfmt_sel.data / 1000
        self.create_fig_ax(title='Mobility Series')
        self.axs[-1].plot(
            df_sel.index, df_sel.values,
            label=self.keywords[kind].replace('_', ' ').title(),
            **self.config['mobility_series'],
        )
        if mark_big_event:
            for kw, val in self.big_event.items():
                if val in date:
                    self.axs[-1].axvline(x=val, **self.config['mobility_series_big_event'])
                    self.axs[-1].text(
                        x=val+pd.Timedelta('5h'), y=0.96*self.axs[-1].get_ylim()[1], s=kw.replace('_', ' '),
                        color=self.config['mobility_series_big_event']['color'], rotation=10)
        if len(df_sel) > 200:
            self.update_fig_ax(fig_width='full')
        self.decorate_axis(ylabel='Mobility Series [$x 10^3$ Times]', xrot=40, yrot=40)
        plt.legend()
        plt.show()


class CovidVisualizer(VisualizerPlus):
    def __init__(self, name='visual_covid'):
        super().__init__(name)
        # In this class, self.dfmt_x = covid data
        self.config = {
            'covid_series': dict(color='dimgrey', linewidth=2),
        }

    def plot_covid_series(self, date, kind='new_confirm'):
        date = handle_date(date)
        assert kind in ('accum_confirm', 'new_confirm', 'infect_rate', 'accum_death', 'new_death', 'fatal_rate')
        dfmt_sel = self.dfmt_x.select_by_date(after=date[0], before=date[-1])
        dfmt_sel = dfmt_sel.select_by_column(include=kind)
        df_sel = dfmt_sel.data
        self.create_fig_ax(title='Covid Statistics Series')
        self.axs[-1].plot(
            df_sel.index, df_sel.values,
            label=kind.replace('_', ' ').title(),
            **self.config['covid_series'],
        )
        if len(df_sel) > 200:
            self.update_fig_ax(fig_width='full')
        self.decorate_axis(ylabel='Covid Statistics Series', xrot=40, yrot=40)
        plt.legend()
        plt.show()


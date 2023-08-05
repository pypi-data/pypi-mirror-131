import warnings
from datetime import datetime
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from pandas import DatetimeIndex

warn = True


class TimeSeriesData:
    def __init__(self, source_data: pd.DataFrame, order_column: str = None):
        self.raw_data = source_data
        if order_column is not None:
            self.indexed_data = self.raw_data.set_index(order_column)
        else:
            self.indexed_data = self.raw_data.copy()
        self.indexed_data = self.indexed_data.sort_index()
        self.grouped_data = None
        self.rolling_widow = None
        self.rolling_trend = None
        self.diff = None
        self.lr_function = None
        self.linear_trend = None

    def set_index(self, order_column: str) -> pd.DataFrame:
        self.indexed_data = self.raw_data.set_index(order_column).sort_index()
        return self.indexed_data

    def set_grouped_data(
            self, order_column, group_window, group_fields=None, agg="mean"
    ):
        grouper = pd.Grouper(key=order_column, freq=group_window)
        if group_fields is not None:
            self.grouped_data = self.raw_data.groupby(grouper)[group_fields]
        else:
            self.grouped_data = self.raw_data.groupby(grouper)
        if agg is not None:
            self.grouped_data = self.grouped_data.agg(agg)
        self.grouped_data = self.grouped_data.sort_index()
        return self.grouped_data

    def set_rolling_trend(self, window, grouped: bool = False, agg="mean"):
        self.rolling_widow = window
        if grouped:
            if self.grouped_data is not None:
                self.rolling_trend = self.grouped_data.rolling(window).agg(agg)
            else:
                raise ValueError(
                    "An attempt to get a moving average on grouped data without first grouping the data."
                )
        else:
            self.rolling_trend = self.indexed_data.rolling(window).agg(agg)
        return self.rolling_trend

    def _get_tts(self, target):
        if target == "grouped":
            tts = self.grouped_data
        elif target == "rolling":
            tts = self.rolling_trend
        elif target == "diff":
            tts = self.diff
        elif target == "linear":
            tts = self.linear_trend
        else:
            if warn and (target != "index"):
                warnings.warn(f"Target is not correct ({target}). Will be used index")
            tts = self.indexed_data

        if tts is None or len(tts) < 2:
            raise ValueError(f"Target data ({target}) is empty.")
        return tts

    def set_diff(
            self, target: str = "index", method: str = "sequential", percent: bool = False
    ):
        tts = self._get_tts(target).copy()
        tts = tts.dropna()
        result = {
            tts.index.name: tts.index
        }
        tts = tts.to_frame(tts) if isinstance(tts, pd.Series) else tts

        if method == "sequential":
            for c in tts.columns:
                tts['next'] = np.array(list(tts[c].iloc[1:].values) + [0])
                result[c] = tts['next'] - tts[c]
                if percent:
                    result[c] = result[c] / tts[c] * 100

        elif method == "end":
            for c in tts.columns:
                result[c] = tts[c].iloc[-1] - tts[c]
                if percent:
                    result[c] = result[c] / tts[c].iloc[-1] * 100
        else:
            raise ValueError(f"Not valid method ({method})")
        self.diff = pd.DataFrame(result).set_index(tts.index.name).sort_index()
        return self.diff

    def set_linear_trend(self, target="index"):
        tts = self._get_tts(target).copy()
        tts = tts.dropna()
        result = {
            tts.index.name: tts.index
        }
        tts = tts.to_frame(tts) if isinstance(tts, pd.Series) else tts

        for c in tts.columns:
            y = tts[c].values.reshape(1, -1)[0]
            x_is_time = isinstance(tts.index, DatetimeIndex)
            try:
                x = (
                    [t.timestamp() for t in tts.index]
                    if x_is_time
                    else tts.index
                )
                self.lr_function = np.poly1d(np.polyfit(x, y, 1))
            except:
                x = range(len(tts))
                self.lr_function = np.poly1d(np.polyfit(x, y, 1))

            result[c] = self.lr_function(x)

        self.linear_trend = pd.DataFrame(result).set_index(tts.index.name).sort_index()
        return self.linear_trend

    def plot(
            self,
            target="index",
            figsize: Tuple[int, int] = (15, 5),
            title: str = None,
            legend=None,
            xticks=None,
            yticks=None,
            xlabel=None,
            ylabel=None,
            save_directory=None
    ):
        plt.figure(figsize=figsize)
        tts = self._get_tts(target)
        plt.plot(tts)
        plt.grid()
        plt.legend(legend)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if xticks is not None:
            plt.xticks(xticks)
        if yticks is not None:
            plt.yticks(yticks)
        if title is not None:
            plt.title(title)
            if save_directory:
                plt.savefig(Path(save_directory) / f"{title}.jpg")
        plt.show()


if __name__ == "__main__":
    # Generate data
    data = pd.DataFrame(
        {
            "time": [datetime.now() + relativedelta(days=i) for i in range(365)],
            "value": [
                np.random.randint(-30, 30) + np.random.randint(-i / 7, i / 3 + 1)
                for i in range(365)
            ],
        }
    )
    # Indexed data
    ts = TimeSeriesData(data, "time")
    ts.plot(title="Indexed data")
    # Grouped data
    ts.set_grouped_data("time", "30d")
    ts.plot(target="grouped", title="Grouped data")
    # Rolling trend
    ts.set_rolling_trend(3, True)
    ts.plot(target="rolling", title="Rolling trend")
    # Linear trend
    ts.set_linear_trend(target="rolling")
    ts.plot(target="linear", title="Linear trend")
    # Diff
    ts.set_diff(target="rolling")
    ts.plot(target="diff", title="Sequential diff of rolling data")
    ts.set_diff(target="rolling", method="end")
    ts.plot(target="diff", title="End diff of rolling data")
    ts.set_linear_trend(target="diff")
    ts.plot(target="linear", title="Linear trend of end dif of rolling data")

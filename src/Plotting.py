import logging
from ChannelAnalysis import ChannelAnalysis
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

class Plotting():

    TEMP_PLOT_NAME: str = "TEMP_PLOT.png"

    def plot_messages_weekday(self, all_channel_analysis: list[ChannelAnalysis]) -> str:
        logging.getLogger().info(f"Plotting messages weekday")
        dfs: dict[str, pd.DataFrame] = {}
        for channel_analysis in all_channel_analysis:
            df: pd.DataFrame = channel_analysis.weekday_number_of_messages().copy()
            if(channel_analysis.current_channels is not None):
                dfs[str(channel_analysis.current_channels)] = df

        day_dict = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }

        ax = None
        for channels, df in dfs.items():
            df["weekday_name"] = df.index.to_series().replace(day_dict)
            ax = df.plot(ax=ax,x="weekday_name", xlabel="Weekday", y="created_at", ylabel="Messages", label=f"{channels}")

        plot_filename = self.TEMP_PLOT_NAME
        plt.savefig(plot_filename)
        plt.close()

        return plot_filename
    
    def plot_messages_percent_weekday(self, all_channel_analysis: list[ChannelAnalysis]) -> str:
        logging.getLogger().info(f"Plotting messages weekday")
        dfs: dict[str, pd.DataFrame] = {}
        for channel_analysis in all_channel_analysis:
            df: pd.DataFrame = channel_analysis.weekday_number_of_messages().copy()
            all_messages_count = df["created_at"].sum()
            if(all_messages_count == 0):
                all_messages_count = 1
            print(df.to_string())
            df["created_at"] = df['created_at']/all_messages_count
            print(df.to_string())
            if(channel_analysis.current_channels is not None):
                dfs[str(channel_analysis.current_channels)] = df

        day_dict = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }

        ax = None
        for channels, df in dfs.items():
            df["weekday_name"] = df.index.to_series().replace(day_dict)
            ax = df.plot(ax=ax,x="weekday_name", xlabel="Weekday", y="created_at", ylabel="Messages", label=f"{channels}", legend=False)

        plot_filename = self.TEMP_PLOT_NAME
        plt.savefig(plot_filename)
        plt.close()

        return plot_filename
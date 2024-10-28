from ChannelAnalysis import ChannelAnalysis
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

class Plotting():

    TEMP_PLOT_NAME: str = "TEMP_PLOT.png"

    def plot_messages_weekday(self, channel_analysis: ChannelAnalysis) -> str:
        df: pd.DataFrame = channel_analysis.weekday_number_of_messages().copy()
        day_dict = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }
        df["weekday_name"] = df.index.to_series().replace(day_dict)
        df.plot(x="weekday_name", xlabel="Weekday", y="content", ylabel="Messages", title="Sent messages by weekday")

        plot_filename = self.TEMP_PLOT_NAME
        plt.savefig(plot_filename)
        plt.close()

        return plot_filename
from ChannelAnalysis import ChannelAnalysis
from Plotting import Plotting

if(__name__ == "__main__"):
    channel_analysis: ChannelAnalysis = ChannelAnalysis()
    plotting: Plotting = Plotting()
    plotting.plot_messages_weekday(channel_analysis)
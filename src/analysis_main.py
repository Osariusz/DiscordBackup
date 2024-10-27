from ChannelAnalysis import ChannelAnalysis

if(__name__ == "__main__"):
    channel_analysis: ChannelAnalysis = ChannelAnalysis()
    t = channel_analysis.number_of_messages_per_channel()
    print(t)
    d = channel_analysis.messages_df
    h = 0
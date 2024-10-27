from ChannelAnalysis import ChannelAnalysis

if(__name__ == "__main__"):
    channel_analysis: ChannelAnalysis = ChannelAnalysis(["example"])
    t = channel_analysis.number_of_messages()
    d = channel_analysis.messages_df
    h = 0
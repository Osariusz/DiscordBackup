import logging
from fastapi import FastAPI, responses
import uvicorn

from ChannelAnalysis import ChannelAnalysis
from Plotting import Plotting
from typing import Callable

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()
main_channel_analysis: ChannelAnalysis

def get_plot(channels: list[int], plot_function):
    all_channel_analysis: list[ChannelAnalysis] = []
    for channel in channels:
        channel_analysis: ChannelAnalysis = ChannelAnalysis(message_df=main_channel_analysis.messages_df)
        channel_analysis.restrict_to_channels([channel])
        all_channel_analysis.append(channel_analysis)
    plot_file: str = plot_function(all_channel_analysis)
    return responses.FileResponse(plot_file)

@app.get('/plot_weekday')
async def get_plot_weekday():
    channels: list[int] = []
    plotting: Plotting = Plotting()
    result: str = get_plot(channels, plotting.plot_messages_percent_weekday)
    return result

@app.get('/plot_weekday_all')
async def get_plot_weekday_all():
    plotting: Plotting = Plotting()
    plot_file: str = plotting.plot_messages_percent_weekday([main_channel_analysis])
    return responses.FileResponse(plot_file)

if __name__ == "__main__":
    logging.info("Preparing data")
    main_channel_analysis = ChannelAnalysis()
    logging.info("Starting the analysis")
    uvicorn.run(app, host="0.0.0.0", port=8000)

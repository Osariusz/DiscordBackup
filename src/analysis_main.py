import logging
from fastapi import FastAPI, responses
import uvicorn

from ChannelAnalysis import ChannelAnalysis
from Plotting import Plotting

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()

@app.get('/plot')
async def get_plot():
    channels = []
    main_channel_analysis: ChannelAnalysis = ChannelAnalysis()
    all_channel_analysis: list[ChannelAnalysis] = []
    for channel in channels:
        channel_analysis: ChannelAnalysis = ChannelAnalysis(message_df=main_channel_analysis.messages_df)
        channel_analysis.restrict_to_channels([channel])
        all_channel_analysis.append(channel_analysis)
    plotting: Plotting = Plotting()
    plot_file: str = plotting.plot_messages_percent_weekday([main_channel_analysis])
    return responses.FileResponse(plot_file)

if __name__ == "__main__":
    logging.info("Starting the analysis")
    uvicorn.run(app, host="0.0.0.0", port=8000)

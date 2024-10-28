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
    channel_analysis: ChannelAnalysis = ChannelAnalysis()
    plotting: Plotting = Plotting()
    plot_file: str = plotting.plot_messages_weekday(channel_analysis)
    return responses.FileResponse(plot_file)

if __name__ == "__main__":
    logging.info("Starting the analysis")
    uvicorn.run(app, host="0.0.0.0", port=8000)

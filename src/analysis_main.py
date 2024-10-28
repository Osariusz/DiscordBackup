from ChannelAnalysis import ChannelAnalysis
from Plotting import Plotting
from fastapi import FastAPI, responses
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from flask import Flask, send_file

app = FastAPI()

@app.get('/plot')
async def get_plot():
    channel_analysis: ChannelAnalysis = ChannelAnalysis()
    plotting: Plotting = Plotting()
    plot_file: str = plotting.plot_messages_weekday(channel_analysis)
    return responses.FileResponse(plot_file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

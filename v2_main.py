from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from pathlib import Path
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

class RTSPRequest(BaseModel):
    rtsp_url: str


# @app.post("/convert_to_hls/")
# def convert_stream(rtsp_url: RTSPRequest):
#     # Define output HLS stream name
#     hls_stream_name = "output.m3u8"

#     # ffmpeg command for conversion (modify as needed)
#     ffmpeg_command = f"ffmpeg -i {rtsp_url} -c:v copy -c:a copy {hls_stream_name}"
#     subprocess.run(ffmpeg_command.split())

#     # Logic for rendering the HLS stream (explained later)

#     return {"message": f"HLS stream generated: {hls_stream_name}"}

@app.post("/convert_to_hls/")
async def convert_to_hls(rtsp_request: RTSPRequest):
    rtsp_url = rtsp_request.rtsp_url
    hls_filename = "stream.m3u8"

    # ffmpeg_command = f"ffmpeg -i {rtsp_url} -c:v copy -c:a copy {hls_filename}"
    
    ffmpeg_command = [
        "ffmpeg",
        "-rtsp_transport", "tcp"
        "-i", rtsp_url,
        "-analyzeduration", "10",
        "-probesize", "128M",
        "-c:v", "copy",
        "-c:a", "copy"
        "-start_number", "1",
        hls_filename
    ]
    # command = ['ffmpeg', '-i', rtsp_url, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-f', 'hls', '-hls_time', '4', '-hls_playlist_type', 'event', 'output.m3u8']
    # command = ['ffmpeg', '-i', rtsp_url, "-analyzeduration", "10", "-probesize", "64M", '-c:v', 'copy', '-c:a', 'aac', "-acodec", "copy", '-strict', 'experimental', '-f', 'hls', '-hls_time', '4', '-hls_playlist_type', 'event', '-s', '1280x720', 'output.m3u8']
    try:
        subprocess.run(ffmpeg_command)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Failed to convert RTSP to HLS")
    
    if not os.path.exists(hls_filename):
        raise HTTPException(status_code=500, detail="Failed to generate HLS stream")
    
    with open(hls_filename, "rb") as file:
        hls_content = file.read()
    
    os.remove(hls_filename)
    
    return {"hls_content": hls_content}


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import ffmpeg
# import os
# app = FastAPI()

# class RTSPRequest(BaseModel):
#     rtsp_url: str

# @app.post("/convert_to_hls/")
# async def convert_to_hls(rtsp_request: RTSPRequest):
#     rtsp_url = rtsp_request.rtsp_url
#     hls_filename = "stream.m3u8"
    
    
#     hls_output = f"{hls_filename}"
    
#     try:

#         input_stream = ffmpeg.input(rtsp_url, rtsp_transport='tcp')

#         output_stream = ffmpeg.output(input_stream, hls_output,
#                                       c='libx265', hls_time=10, hls_list_size=6,
#                                       hls_wrap=10, start_number=1, preset='ultrafast')
        
#         ffmpeg.run(output_stream)
#     except ffmpeg.Error as e:
#         raise HTTPException(status_code=500, detail="Failed to convert RTSP to HLS")
    
#     with open(hls_output, "rb") as file:
#         hls_content = file.read()
    
#     os.remove(hls_output)
    
#     return {"hls_content": hls_content}
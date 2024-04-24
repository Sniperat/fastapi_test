from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.post("/convert")
async def convert_rtsp_to_hls(rtsp_url: str):
    # Команда для вызова ffmpeg для конвертации RTSP в HLS
    command = ['ffmpeg', '-i', rtsp_url, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-f', 'hls', '-hls_time', '4', '-hls_playlist_type', 'event', 'output.m3u8']
    # Запуск ffmpeg
    subprocess.run(command)
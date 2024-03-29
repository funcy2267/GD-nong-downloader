import yt_dlp
import requests
import os
from io import BytesIO
from zipfile import ZipFile

def selectPath():
    global gd_music
    print("Select song location:")
    path_names = ["Default", "Alternative", "Custom"]
    paths = ['%localappdata%/GeometryDash/', '%programfiles(x86)%/Steam/steamapps/common/Geometry Dash/Resources', 'Select']
    i=1
    for path in path_names:
        print(str(i)+". "+path+" ["+paths[i-1]+"]")
        i+=1
    answer = input("[1] ")
    if answer in ["1", ""]:
        gd_music = paths[0]
    elif answer == "2":
        gd_music = paths[1]
    elif answer == "3":
        gd_music = input("Custom path: ")
    print("Selected path: "+gd_music)

def downloadFfmpeg():
    print("Downloading...")
    r = requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
    print("Unpacking...")
    with ZipFile(BytesIO(r.content)) as zf, open("ffmpeg.exe", "wb") as f:
        f.write(zf.read(zf.namelist()[0]+'bin/ffmpeg.exe'))
    print("ffmpeg successfully downloaded.")

def downloadSong(song_link, song_id):
    ydl_opts = {
        'format': 'mp3/bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': gd_music+song_id
    }
    print("Downloading song...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_link])
    print("Song downloaded.")

def dlProcess():
    song_link = input("Enter song link: ")
    song_id = input("Enter song ID: ")
    downloadSong(song_link, song_id)
    if input("Do you want to download next song? [y/n] ") == "y":
        dlProcess()

def checkFfmpeg():
    if not os.path.exists("ffmpeg.exe"):
        if input("ffmpeg not detected in current path. Do you want to download it now to the current directory? [y/n] ") == "y":
            downloadFfmpeg()

checkFfmpeg()
selectPath()
dlProcess()

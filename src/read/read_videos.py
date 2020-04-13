import os
import datetime
import pathlib

project_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
dir = f"output/{datetime.date.today().strftime('%Y-%m-%d')}"
absolute_dir = os.path.join(project_path, dir)

for video in os.listdir(absolute_dir):
    cmd = os.startfile(os.path.join(absolute_dir, video))

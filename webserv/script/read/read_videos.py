import os
import datetime
from utils.config import PROJECT_PATH


dir = f"output/{datetime.date.today().strftime('%Y-%m-%d')}"
absolute_dir = os.path.join(PROJECT_PATH, dir)

for video in [v for v in os.listdir(absolute_dir) if v.endswith(".mp4")]:
    cmd = os.startfile(os.path.join(absolute_dir, video))

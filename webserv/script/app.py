import os
from utils.config import PROJECT_PATH


scrap_script = os.path.join(PROJECT_PATH, "webserv", "script", "scrap", "scrap_articles.py")

#os.system(f"{scrap_script} COVID-19")
#os.system(f"{scrap_script} FOOTBALL")

generate_script = os.path.join(PROJECT_PATH, "webserv", "script", "generate", "generate_video.py")

#os.system(f"{generate_script} COVID-19 youtube")
#os.system(f"{generate_script} COVID-19 instagram")
#os.system(f"{generate_script} COVID-19 tiktok")

#os.system(f"{generate_script} FOOTBALL youtube")
#os.system(f"{generate_script} FOOTBALL instagram")
#os.system(f"{generate_script} FOOTBALL tiktok")

upload_youtube_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_youtube.py")
upload_twitter_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_twitter.py")

#os.system(f"{upload_youtube_script} COVID-19")
#os.system(f"{upload_twitter_script} COVID-19")

os.system(f"{upload_youtube_script} FOOTBALL")
os.system(f"{upload_twitter_script} FOOTBALL")

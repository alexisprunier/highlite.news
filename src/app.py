import os
from utils.config import PROJECT_PATH


os.system("scrap_articles.py COVID-19")
os.system("scrap_articles.py FOOTBALL")

generate_script = os.path.join(PROJECT_PATH, "src", "generate", "generate_video.py")

os.system(f"{generate_script} COVID-19 youtube")
os.system(f"{generate_script} COVID-19 instagram")
os.system(f"{generate_script} COVID-19 tiktok")

os.system(f"{generate_script} FOOTBALL youtube")
os.system(f"{generate_script} FOOTBALL instagram")
os.system(f"{generate_script} FOOTBALL tiktok")

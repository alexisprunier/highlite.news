import os
from utils.config import PROJECT_PATH

generate_script = os.path.join(PROJECT_PATH, "src", "generate", "generate_video.py")

#os.system("scrap_articles.py")
os.system(f"{generate_script} youtube")
os.system(f"{generate_script} instagram")
os.system(f"{generate_script} tiktok")
os.system(f"{generate_script} snapchat")

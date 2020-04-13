import os
import pathlib

project_path = str(pathlib.Path(__file__).parent.absolute())
generate_script = os.path.join(project_path, "generate", "generate_video.py")

#os.system("scrap_articles.py")
os.system(f"{generate_script} youtube")
os.system(f"{generate_script} instagram")
os.system(f"{generate_script} tiktok")

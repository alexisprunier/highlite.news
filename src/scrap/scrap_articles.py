from bs4 import BeautifulSoup
import re
from selenium import webdriver
import json
import pathlib
import os
from urllib import request
from PIL import Image
import datetime
import random
import imghdr
from utils.config import PROJECT_PATH
from db import db
import sys


def traverse(source, base_url, soup, level):
	if soup.name is not None:
		if level >= 4:
			urls = re.findall(r"(?:http|ftp|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?", str(soup))
			paragraphs = [p for p in re.findall(r"(?<=>)[0-9A-Za-zÀ-ÖØ-öø-ÿ ’,.;:'\n&]{40,200}(?=<)", str(soup)) if len(p.strip()) > 0]
			times = re.findall(r"(?<=>)(?:[01][0-9]|2[0-3])[:h][0-5][0-9](?=<)", str(soup))
			image_tags = soup.findAll('img')
			
			urls = [u for u in urls if u[-4:] not in [".jpg", ".png", ".JPG", ".PNG"]]
			
			if len(image_tags) == 1 and len(paragraphs) >= 1 and len(times) <= 1:
				if "src" in image_tags[0]:
					image = image_tags[0]['src']
					
					if image.startswith("/"):
						image = os.path.join(base_url, image)
				else:
					image = re.findall(r"(?:http|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?", str(image_tags[0]))
					
					if len(image) > 0:
						image = image[0]
					else:
						image = None
					
				articles.append({
					"title": paragraphs[0].strip(),
					"source.json": source,
					"link": urls[0] if len(urls) > 0 else None,
					"image_url": image,
					"time": times[0] if len(times) > 0 else None
				})
		
		for child in soup.children:
			if child.name is not None:
				traverse(source, base_url, child, level + 1)


articles = []
category = sys.argv[1]
sources = db.read("source")
filters = db.read("filter")

if category in sources:
	sources = sources[category]
else:
	print("category not found in sources, review argument 1")
	exit()

if category in filters:
	filters = filters[category]
else:
	print("category not found in filters, review argument 1")
	exit()

current_path = str(pathlib.Path(__file__).parent.absolute())
dir = os.path.join(PROJECT_PATH, "data", datetime.date.today().strftime('%Y-%m-%d'))

if not os.path.exists(dir):
	os.mkdir(dir)

# Get the articles

if not os.path.exists(os.path.join(dir, f"articles_{category}.json")):

	for source in sources:
		driver = webdriver.Chrome(executable_path=r"C:\Users\pruni\Desktop\Highlite.news\bin\chromedriver.exe")
		driver.get(source["url"])
		html = driver.page_source
		soup = BeautifulSoup(html)
		[x.extract() for x in soup.find_all('noscript')]
		traverse(source["source"], source["url"], soup, 0)

	with open(os.path.join(dir, f"articles_{category}.json"), 'w') as outfile:
		json.dump(articles, outfile, indent=4)

else:
	articles = json.load(open(os.path.join(dir, f"articles_{category}.json"), "r"))

# Filter the articles

articles = [a for a in articles if a["image_url"] is not None]

if "contain" in filters:
	articles = [a for a in articles if len([_ for _ in filters["contain"] if _ in a["title"].lower()]) > 0]

articles = [a for i, a in enumerate(articles) if i == [y for y, b in enumerate(articles) if a["title"] == b["title"]][0]]

random.shuffle(articles)

# Get the images

if not os.path.exists(os.path.join(dir, 'img')):
	os.mkdir(os.path.join(dir, 'img'))

for i, article in enumerate(articles):
	saved_image = os.path.join(dir, 'img', article['image_url'].split('?')[0].split('/')[-1])
	if not os.path.exists(saved_image):
		try:
			request.urlretrieve(article["image_url"], saved_image)
		except Exception as e:
			print(e, "ON THIS URL :", article["image_url"])
			saved_image = None

	image_type = imghdr.what(saved_image) if saved_image is not None else None

	if image_type is not None:
		if image_type in ("jpg", "jpeg"):
			im = Image.open(saved_image)
			saved_image = (".".join(saved_image.split(".")[:-1]) if "." in saved_image[-5:] else saved_image) + ".png"
			im.save(saved_image, "JPEG")

		article["image"] = saved_image
	else:
		article["image"] = None

articles = [a for a in articles if a["image"] is not None]

# Save the data

with open(os.path.join(dir, f"articles_{category}_filtered.json"), 'w') as outfile:
	json.dump(articles, outfile, indent=4)

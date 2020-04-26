from bs4 import BeautifulSoup
import re
from selenium import webdriver
import os
from urllib import request
from PIL import Image
import random
import imghdr
import sys
import datetime
from db.db import DB
import json
from utils.config import PROJECT_PATH
from io import BytesIO
import io


def traverse(source, category, base_url, soup, level):
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
					"title": paragraphs[0].replace("\n", "").strip(),
					"source": source,
					"category": category,
					"url": urls[0] if len(urls) > 0 else None,
					"image_url": image,
					"publication_time": times[0] if len(times) > 0 else None,
					"scrap_date": datetime.date.today()
				})
		
		for child in soup.children:
			if child.name is not None:
				traverse(source, category, base_url, child, level + 1)


# Controle the arguments

articles = []
category = sys.argv[1]
sources = json.load(open(os.path.join(PROJECT_PATH, "db", "source.json")))
filters = json.load(open(os.path.join(PROJECT_PATH, "db", "filter.json")))

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

# Get the articles

for source in sources:
	driver = webdriver.Chrome(executable_path=r"C:\Users\pruni\Desktop\Highlite.news\bin\chromedriver.exe")
	driver.get(source["url"])
	html = driver.page_source
	soup = BeautifulSoup(html)
	[x.extract() for x in soup.find_all('noscript')]
	traverse(source["source"], category, source["url"], soup, 0)

# Filter the articles

articles = [a for a in articles if a["image_url"] is not None]

if "contain" in filters:
	articles = [a for a in articles if len([_ for _ in filters["contain"] if _ in a["title"].lower()]) > 0]

articles = [a for i, a in enumerate(articles) if i == [y for y, b in enumerate(articles) if a["title"] == b["title"]][0]]

random.shuffle(articles)

# Get the images

for i, article in enumerate(articles):
	image = None
	print("0", article["title"])

	try:
		#image, _ = request.urlretrieve(article["image_url"])
		with request.urlopen(article["image_url"]) as response:
			image = response.read()
		print("A", image)
	except Exception as e:
		image = None
		print(e, "ON THIS URL :", article["image_url"])

	image_type = imghdr.what(None, image) if image is not None else None
	print("B", image_type)

	if image_type is not None:
		if image_type in ("jpg", "jpeg"):
			im = Image.open(io.BytesIO(image))
			with BytesIO() as f:
				im.save(f, format='JPEG')
				image = f.getvalue()
			article["image"] = image
		elif image_type == "png":
			article["image"] = image
		else:
			print("Image type not accepted", image_type)
			article["image"] = None
	else:
		article["image"] = None

	print("C", article["image"])

articles = [a for a in articles if a["image"] is not None]

# Save the data

if len(articles) > 0:
	db = DB()

	for article in articles:

		a = db.get(db.tables["Article"], {"title": article["title"]})

		if len(a) == 0:
			db.merge(article, db.tables["Article"])
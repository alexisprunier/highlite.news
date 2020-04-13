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


articles = []


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
					"source": source,
					"link": urls[0] if len(urls) > 0 else None,
					"image_url": image,
					"time": times[0] if len(times) > 0 else None
				})
		
		for child in soup.children:
			if child.name is not None:
				traverse(source, base_url, child, level + 1)


pages = [
	("Ouest France", "https://www.lemonde.fr/"),
	("Ouest France", "https://www.liberation.fr/"),
	("Les Echos", "https://www.lesechos.fr/"),
	("Le Figaro", "https://www.lefigaro.fr/"),
	("Le Parisien", "http://www.leparisien.fr/"),
	("20 Minutes", "https://www.20minutes.fr/"),
	("La Tribune", "https://www.latribune.fr/"),
]

current_path = str(pathlib.Path(__file__).parent.absolute())
dir = f"data/{datetime.date.today().strftime('%Y-%m-%d')}"

if not os.path.exists(dir):
	os.mkdir(dir)

# Get the articles

if not os.path.exists(os.path.join(dir, "articles.json")):

	for source, url in pages:
		driver = webdriver.Chrome(executable_path=r"C:\Users\pruni\Desktop\Highlite.news\bin\chromedriver.exe")
		driver.get(url)
		html = driver.page_source
		soup = BeautifulSoup(html)
		[x.extract() for x in soup.find_all('noscript')]
		traverse(source, url, soup, 0)

	with open(os.path.join(dir, "articles.json"), 'w') as outfile:
		json.dump(articles, outfile, indent=4)

else:
	articles = json.load(open(os.path.join(dir, "articles.json"), "r"))

# Filter the articles

articles = [a for a in articles if a["image_url"] is not None]
articles = [a for a in articles if "covid" in a["title"].lower() or "coronavirus" in a["title"].lower()]
articles = [a for i, a in enumerate(articles) if i == [y for y, b in enumerate(articles) if a["title"] == b["title"]][0]]

random.shuffle(articles)
articles = articles[:10] if len(articles) > 9 else articles

# Get the images

for article in articles:
	saved_image = os.path.join(dir, article['image_url'].split('?')[0].split('/')[-1])
	request.urlretrieve(article["image_url"], saved_image)
	image_type = imghdr.what(saved_image)

	if image_type in ("jpg", "jpeg"):
		im = Image.open(saved_image)
		im.save(saved_image.split(".")[0] + ".png", "JPEG")

	article["image"] = saved_image[:-4] + ".png"

# Save the data

with open(os.path.join(dir, "articles_filt.json"), 'w') as outfile:
	json.dump(articles, outfile, indent=4)

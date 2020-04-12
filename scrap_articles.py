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


articles = []


def traverse(base_url, soup, level):
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
					"title": paragraphs[0],
					"link": urls[0] if len(urls) > 0 else None,
					"image_url": image,
					"time": times[0] if len(times) > 0 else None
				})
		
		for child in soup.children:
			if child.name is not None:
				traverse(base_url, child, level + 1)


pages = [
	#"https://www.ouest-france.fr/",
	#"https://www.ouest-france.fr/monde/",
	#"https://www.ouest-france.fr/economie/entreprises",
	"https://www.lemonde.fr/",
	#"https://www.lemonde.fr/economie-francaise/",
	#"https://www.lemonde.fr/international/",
	#"https://www.lemonde.fr/politique/",
	#"https://www.lemonde.fr/sport/",
	"https://www.liberation.fr/",
	"https://www.lesechos.fr/",
	"https://www.lefigaro.fr/",
	"http://www.leparisien.fr/",
	"https://www.20minutes.fr/",
	"https://www.latribune.fr/",
]


current_path = str(pathlib.Path(__file__).parent.absolute())

for page in pages:
	driver = webdriver.Chrome(executable_path=r"C:\Users\pruni\Desktop\Highlite.news\bin\chromedriver.exe")
	driver.get(page)
	html = driver.page_source
	soup = BeautifulSoup(html)
	[x.extract() for x in soup.find_all('noscript')]
	traverse(page, soup, 0)

dir = f"data/{datetime.date.today().strftime('%Y-%m-%d')}"

if not os.path.exists(dir):
	os.mkdir(dir)

articles = [a for a in articles if a["image_url"] is not None]
articles = [a for a in articles if "covid" in a["title"].lower() or "coronavirus" in a["title"].lower()]
random.shuffle(articles)
articles = articles[:10] if len(articles) > 9 else articles

for article in articles:
	saved_image = os.path.join(dir, article['image_url'].split('?')[0].split('/')[-1])
	request.urlretrieve(article["image_url"], saved_image)

	if saved_image.lower().endswith(".jpg"):
		im = Image.open(saved_image)
		im.save(saved_image[-4] + ".png", "JPEG")

	article["image"] = saved_image[-4] + ".png"

with open(os.path.join(dir, "articles.json"), 'w') as outfile:
	json.dump(articles, outfile, indent=4)

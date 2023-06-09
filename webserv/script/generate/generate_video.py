import cv2
import os
import datetime
from utils.modify_image import apply_dark_effect, resize_image, crop_image_in_center
from utils.overlay_image import overlay_image, overlay_highlight_frame, overlay_text
from mhmovie.code import movie, music
from utils.read_image import read_webp
import copy
from PIL import Image, ImageFont, ImageDraw
import math
import subprocess
from utils.config import PROJECT_PATH, ENVIRONMENT
import numpy as np
from webserv.exception.already_generated import AlreadyGeneratedException


class GenerateVideo:

	@staticmethod
	def run(db, category, format):

		conf = {
			"youtube": {
				"format": (1920, 1080),
				"padding": 130,
				"title1": {
					"size": 300,
					"pos": ("centered", 430),
				},
				"title2": {
					"size": 70,
					"pos": ("centered", 380)
				},
				"intro_date": {
					"size": 150,
					"pos": (1920 - 40, 1080 - 170),
				},
				"theme": {
					"size": 120,
					"pos": (1920 - 130, 60),
					"max_width": 10000,
				},
				"date": {
					"size": 50,
					"pos": (1920 - 130, 1080 - 120),
				},
				"circle": {
					"size": 16,
					"pos": (lambda i, total: (int(130 + (60 * i)), 1080 - 92)),
				},
				"article": {
					"image_pos": ("centered", 250),
					"image_height": 450,
					"title_pos": ("centered", 750),
					"title_max_width": 45,
					"font_size": 50
				},
				"social": {
					"pos1": (int(1920 / 2 - 600), 430),
					"pos2": (int(1920 / 2 - 200), 430),
					"pos3": (int(1920 / 2 + 200), 430),
					"pos4": (int(1920 / 2 + 600), 430)
				},
				"ad": {
					"size": 45,
					"pos": (1920 - 130, 90),
					"max_width": 10000,
				},
			},
			"instagram": {
				"format": (1080, 1080),
				"padding": 70,
				"title1": {
					"size": 140,
					"pos": ("centered", 500),
				},
				"title2": {
					"size": 55,
					"pos": ("centered", 450)
				},
				"intro_date": {
					"size": 50,
					"pos": ("centered", 890),
				},
				"theme": {
					"size": 50,
					"pos": (1080 - 70, 200),
					"max_width": 23,
				},
				"date": {
					"size": 50,
					"pos": ("centered", 890),
				},
				"circle": {
					"size": 16,
					"pos": (lambda i, total: (int(1080 / 2 - (total * 60 / 2) + (i * 60) + 30), 990)),
				},
				"article": {
					"image_pos": ("centered", 320),
					"image_height": 350,
					"title_pos": ("centered", 720),
					"title_max_width": 40,
					"font_size": 35
				},
				"social": {
					"pos1": (330, 340),
					"pos2": (750, 340),
					"pos3": (330, 600),
					"pos4": (750, 600)
				},
				"ad": {
					"size": 35,
					"pos": (1080 - 70, 200),
					"max_width": 30,
				},
			},
			"snapchat": {
				"format": (1080, 1920),
				"padding": 70,
				"title1": {
					"size": 170,
					"pos": ("centered", 820),
				},
				"title2": {
					"size": 60,
					"pos": ("centered", 750)
				},
				"intro_date": {
					"size": 70,
					"pos": ("centered", 1620),
				},
				"theme": {
					"size": 120,
					"pos": (1080 - 70, 250),
					"max_width": 30,
				},
				"date": {
					"size": 70,
					"pos": ("centered", 1600),
				},
				"circle": {
					"size": 16,
					"pos": (lambda i, total: (int(1080 / 2 - (total * 80 / 2) + (i * 80) + 30), 1800)),
				},
				"article": {
					"image_pos": ("centered", 580),
					"image_height": 400,
					"title_pos": ("centered", 1100),
					"title_max_width": 27,
					"font_size": 55
				},
				"social": {
					"pos1": (340, 700),
					"pos2": (740, 700),
					"pos3": (340, 1150),
					"pos4": (740, 1150)
				},
				"ad": {
					"size": 70,
					"pos": (1080 - 70, 250),
					"max_width": 20,
				},
			},
			"tiktok": {
				"format": (1080, 1920),
				"padding": 70,
				"title1": {
					"size": 170,
					"pos": ("centered", 820),
				},
				"title2": {
					"size": 60,
					"pos": ("centered", 750)
				},
				"intro_date": {
					"size": 70,
					"pos": ("centered", 1620),
				},
				"theme": {
					"size": 120,
					"pos": (1080 - 70, 250),
					"max_width": 30,
				},
				"date": {
					"size": 55,
					"pos": ("centered", 1620),
				},
				"circle": {
					"size": 16,
					"pos": (lambda i, total: (int(1080 / 2 - (total * 80 / 2) + (i * 80) + 30), 1800)),
				},
				"article": {
					"image_pos": ("centered", 580),
					"image_height": 400,
					"title_pos": ("centered", 1100),
					"title_max_width": 27,
					"font_size": 55
				},
				"social": {
					"pos1": (340, 700),
					"pos2": (740, 700),
					"pos3": (340, 1150),
					"pos4": (740, 1150)
				},
				"ad": {
					"size": 70,
					"pos": (1080 - 70, 250),
					"max_width": 20,
				},
			}
		}

		if format in conf:
			conf = conf[format]
		else:
			raise Exception(f"The second argument is not amongst {', '.join(conf.keys())}")

		####################
		# INIT
		####################

		# Get the articles

		pipeline = db.get(db.tables["Pipeline"], {"category": category})
		pipeline = pipeline[0] if len(pipeline) > 0 else None
		if pipeline is None:
			raise Exception("Pipeline not found for this category")
		articles = db.get_articles_of_the_day(category)

		if len(articles) < 3:
			raise Exception("Not enough article")

		# init paths

		output_dir = os.path.join(PROJECT_PATH, "output")

		if not os.path.exists(output_dir):
			os.mkdir(output_dir)

		output_dir = os.path.join(PROJECT_PATH, "output", datetime.date.today().strftime('%Y-%m-%d'))

		if not os.path.exists(output_dir):
			os.mkdir(output_dir)

		avi_video_name = f'highlite_{category.replace(" ", "")}_{format}_{datetime.date.today().strftime("%Y-%m-%d")}.avi'
		mp4_video_name = f"{avi_video_name.split('.')[0]}.mp4"
		tmp_mp4_video_name = f"tmp_{avi_video_name.split('.')[0]}.mp4"
		avi_video_rel_path = f'{output_dir}/{avi_video_name}'
		mp4_video_rel_path = f'{output_dir}/{mp4_video_name}'
		tmp_mp4_video_rel_path = f'{output_dir}/{tmp_mp4_video_name}'
		avi_video_abs_path = os.path.join(PROJECT_PATH, avi_video_rel_path)
		mp4_video_abs_path = os.path.join(PROJECT_PATH, mp4_video_rel_path)
		tmp_mp4_video_abs_path = os.path.join(PROJECT_PATH, tmp_mp4_video_rel_path)

		if os.path.exists(mp4_video_abs_path):
			raise AlreadyGeneratedException("The video already exists")

		video_width = conf["format"][0]
		video_height = conf["format"][1]

		fourcc = cv2.VideoWriter_fourcc(*'DIVX')
		video = cv2.VideoWriter(avi_video_rel_path, fourcc, 24, (video_width, video_height))

		color_yellow = (243, 242, 121)
		color_dark_yellow = (255, 204, 64)
		color_blue = (151, 242, 243)
		color_dark_blue = (55, 196, 255)

		color_bgr_yellow = (151, 242, 243)
		color_bgr_dark_yellow = (64, 204, 255)
		color_bgr_blue = (243, 242, 151)
		color_bgr_dark_blue = (255, 196, 55)

		today = datetime.date.today().strftime("%d-%m-%Y")

		####################
		# CREATE DEFAULT FRAME
		####################

		img_background = cv2.imread(os.path.join(PROJECT_PATH, 'static', 'img', 'background', f"background_{category.replace(' ', '')}.jpg"), -1)
		if conf["format"][0] > len(img_background[0]) or conf["format"][1] > len(img_background):
			img_background = resize_image(img_background, 2)
		img_background = crop_image_in_center(img_background, video_width, video_height)
		img_logo = cv2.imread(os.path.join(PROJECT_PATH, 'static/img/logo/Highlite125x400.png'), -1)

		default_frame = apply_dark_effect(img_background)
		default_frame = overlay_highlight_frame(img_background)
		default_frame = overlay_image(default_frame, img_logo, (50, 50))

		# Add the circles

		circle_positions = []

		for i in range(0, len(articles)):
			default_frame = cv2.circle(default_frame, conf["circle"]["pos"](i, len(articles)), conf["circle"]["size"], color_bgr_yellow, -1)

		####################
		# GENERATE THE INTRO
		####################

		image_intro = copy.copy(default_frame)

		font = ImageFont.truetype(os.path.join(PROJECT_PATH, "static/font/bungee/Bungee-Regular.otf"), 300)
		img_pil = Image.fromarray(default_frame)
		draw = ImageDraw.Draw(img_pil)
		w, h = draw.textsize(category, font=font)
		txt = f"Les {len(articles)} articles du jour sur"

		for n in range(4 * 24):
			if n == 0:
				n = 400
			image_intro = overlay_text(default_frame, txt, conf["title2"]["pos"], conf["title2"]["size"], color_bgr_dark_yellow, f=n)
			image_intro = overlay_text(image_intro, category, conf["title1"]["pos"], conf["title1"]["size"], color_bgr_dark_yellow, f=n)
			image_intro = overlay_text(image_intro, today, conf["intro_date"]["pos"], conf["intro_date"]["size"], color_bgr_blue, pos_type="right", f=n)
			video.write(image_intro)

		####################
		# GENERATE ARTICLES
		####################

		frame = copy.copy(default_frame)

		frame = overlay_text(frame, category, conf["theme"]["pos"], conf["theme"]["size"], color_bgr_dark_yellow, pos_type="right")
		frame = overlay_text(frame, today, conf["date"]["pos"], conf["date"]["size"], color_bgr_blue, pos_type="right")

		images_splash = read_webp(os.path.join(PROJECT_PATH, 'static/img/splash1.webp'))

		# Generate for each article

		for i, article in enumerate(articles):

			frame_article = cv2.circle(frame, conf["circle"]["pos"](i, len(articles)), conf["circle"]["size"], color_bgr_blue, -1)
			default_frame = cv2.circle(default_frame, conf["circle"]["pos"](i, len(articles)), conf["circle"]["size"], color_bgr_blue, -1)

			image_logo = cv2.imdecode(np.frombuffer(article.image, np.uint8), cv2.IMREAD_COLOR)

			if image_logo is not None:

				for y, _ in enumerate(range(5 * 24)):
					frame_a = copy.copy(frame_article)

					# Add the content

					frame_a = overlay_text(frame_a, article.title, conf["article"]["title_pos"], conf["article"]["font_size"], color_bgr_blue, max_width=conf["article"]["title_max_width"], f=y)
					image_logo = resize_image(image_logo, conf["article"]["image_height"] / image_logo.shape[0])
					frame_a = overlay_image(frame_a, image_logo, conf["article"]["image_pos"], f=y)

					if math.ceil(y / 1.5) < len(images_splash):
						position_splash = (conf["circle"]["pos"](i, len(articles))[0] - 40, conf["circle"]["pos"](i, len(articles))[1] - 40)
						image_article_with_splash = overlay_image(frame_a, images_splash[math.ceil(y / 1.5)], position_splash)

					video.write(frame_a)

		####################
		# GENERATE THE OUTRO
		####################

		frame = copy.copy(default_frame)

		image_twitter = cv2.imread(os.path.join(PROJECT_PATH, "static/img/social-network/twitter512x512.png"), cv2.IMREAD_UNCHANGED)
		image_twitter = resize_image(image_twitter, 0.25)
		image_tiktok = cv2.imread(os.path.join(PROJECT_PATH, "static/img/social-network/tiktok512x512.png"), cv2.IMREAD_UNCHANGED)
		image_tiktok = resize_image(image_tiktok, 0.25)
		image_instagram = cv2.imread(os.path.join(PROJECT_PATH, "static/img/social-network/instagram512x512.png"), cv2.IMREAD_UNCHANGED)
		image_instagram = resize_image(image_instagram, 0.25)
		image_snapchat = cv2.imread(os.path.join(PROJECT_PATH, "static/img/social-network/snapchat128x128.png"), cv2.IMREAD_UNCHANGED)

		pos_el1 = int(video_width / 2 - 600)
		pos_el2 = int(video_width / 2 - 200)
		pos_el3 = int(video_width / 2 + 200)
		pos_el4 = int(video_width / 2 + 600)

		for y, _ in enumerate(range(6 * 24)):
			txt = "Liens sur: www.highlite.news"
			frame = overlay_text(default_frame, txt, conf["date"]["pos"], conf["date"]["size"], color_bgr_blue, pos_type="right", f=max(0, y))
			txt = f"Nouvelle vidéo {category} tous les jours à {pipeline.publication_time[:2] if pipeline.publication_time is not None else 'XX'}h"
			frame = overlay_text(frame, txt, conf["ad"]["pos"], conf["ad"]["size"], color_bgr_dark_yellow, pos_type="right", max_width=conf["ad"]["max_width"])

			frame = overlay_image(frame, image_twitter, conf["social"]["pos1"], pos_type="middle", f=max(0, y))
			frame = overlay_image(frame, image_instagram, conf["social"]["pos2"], pos_type="middle", f=max(0, y-8))
			frame = overlay_image(frame, image_snapchat, conf["social"]["pos3"], pos_type="middle", f=max(0, y-16))
			frame = overlay_image(frame, image_tiktok, conf["social"]["pos4"], pos_type="middle", f=max(0, y-24))

			twitter_tag_pos = (conf["social"]["pos1"][0], conf["social"]["pos1"][1] + 170)
			instagram_tag_pos = (conf["social"]["pos2"][0], conf["social"]["pos2"][1] + 170)
			snapchat_tag_pos = (conf["social"]["pos3"][0], conf["social"]["pos3"][1] + 170)
			tiktok_tag_pos = (conf["social"]["pos4"][0], conf["social"]["pos4"][1] + 170)

			fr = overlay_text(frame, "@highlitenews", twitter_tag_pos, 30, color_bgr_blue, pos_type="middle", f=max(0, y))
			fr = overlay_text(fr, "@highlite.news", instagram_tag_pos, 30, color_bgr_blue, pos_type="middle", f=max(0, y-8))
			fr = overlay_text(fr, "@highlite.news", snapchat_tag_pos, 30, color_bgr_blue, pos_type="middle", f=max(0, y-16))
			fr = overlay_text(fr, "@highlite.news", tiktok_tag_pos, 30, color_bgr_blue, pos_type="middle", f=max(0, y-24))

			video.write(fr)

		####################
		# GET THE VIDEO OUT !
		####################

		cv2.destroyAllWindows()
		video.release()

		####################
		# ADD MUSIC
		####################

		movie_path = avi_video_abs_path.replace("\\", "/") if ENVIRONMENT != "dev" else avi_video_abs_path

		mov = movie.__new__(movie)
		mov.fp = movie_path
		mov.folder = os.path.dirname(movie_path)
		mov.type = os.path.splitext(movie_path)[1]
		mov.music_fp = None
		mov.del_files = []

		music_path = os.path.join(PROJECT_PATH, f'static/sound/sound_{category.replace(" ", "")}.mp3')
		music_path = music_path.replace("\\", "/") if ENVIRONMENT != "dev" else music_path

		"""mus = music.__new__(music)
		mus.fp = music_path
		mus.type = os.path.splitext(music_path)[1]
		mus.folder = os.path.dirname(music_path)
		mus.del_files = []"""

		mov.music_fp = music_path
		mov.save(tmp_mp4_video_abs_path.replace("\\", "/") if ENVIRONMENT != "dev" else tmp_mp4_video_abs_path)

		if os.path.exists(mp4_video_abs_path):
			os.remove(mp4_video_abs_path)

		subprocess.call(['ffmpeg',
							'-i',
							tmp_mp4_video_abs_path.replace("\\", "/") if ENVIRONMENT != "dev" else tmp_mp4_video_abs_path,
							'-y',
							'-nostdin',
							'-ss',
							'0',
							'-t',
							str(10 + len(articles) * 5),
							mp4_video_abs_path.replace("\\", "/") if ENVIRONMENT != "dev" else mp4_video_abs_path])

		####################
		# CLEAN
		####################

		if os.path.exists(avi_video_abs_path):
			os.remove(avi_video_abs_path)
		if os.path.exists(tmp_mp4_video_abs_path):
			os.remove(tmp_mp4_video_abs_path)

		####################
		# SNAPCHAT SPLIT WITH THE TIKTOK FORMAT
		####################

		"""if format == "tiktok":
			split = [4] + [5 for _ in articles] + [6]
			start_time = 0
		
			for i, s in enumerate(split):
				output_name = f"{'.'.join(mp4_video_abs_path.split('.')[:-1])}_{i+1}.mp4".replace("tiktok", "snapchat")
				subprocess.call(['ffmpeg', '-i', mp4_video_abs_path, '-y', '-nostdin', '-ss', str(start_time), '-t', str(s), output_name])
				start_time += s
		"""

		####################
		# CREATE A VIDEO RECORD ON DB
		####################

		video = db.merge({
			"title": f"Highlite du {today} sur {pipeline.article} {category}",
			"file_name": mp4_video_abs_path,
			"format": format,
			"category": category,
			"creation_date": datetime.date.today()
		}, db.tables["Video"])

		db.merge([
			{"video_id": video.id, "article_id": a.id, "pos": i+1} for i, a in enumerate(articles)
		], db.tables["VideoArticle"])

		db.session.close()

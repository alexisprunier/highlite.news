import cv2
import os
import datetime
import json
from utils.modify_image import apply_dark_effect, resize_image, crop_image_in_center
from utils.overlay_image import overlay_image, overlay_highlight_frame, overlay_text
from utils.read_image import read_webp
import copy
from PIL import Image, ImageFont, ImageDraw
import math
import sys
import ffmpeg
import pathlib


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
		"format": (800, 1000),
		"padding": 70,
		"title1": {
			"size": 120,
			"pos": ("centered", 490),
		},
		"title2": {
			"size": 40,
			"pos": ("centered", 450)
		},
		"intro_date": {
			"size": 30,
			"pos": ("centered", 840),
		},
		"theme": {
			"size": 50,
			"pos": (800 - 70, 200),
			"max_width": 23,
		},
		"date": {
			"size": 30,
			"pos": ("centered", 840),
		},
		"circle": {
			"size": 16,
			"pos": (lambda i, total: (int(800 / 2 - (total * 60 / 2) + (i * 60) + 30), 920)),
		},
		"article": {
			"image_pos": ("centered", 320),
			"image_height": 350,
			"title_pos": ("centered", 720),
			"title_max_width": 45,
			"font_size": 25
		},
		"social": {
			"pos1": (230, 320),
			"pos2": (570, 320),
			"pos3": (230, 570),
			"pos4": (570, 570)
		},
		"ad": {
			"size": 35,
			"pos": (800 - 70, 200),
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
			"size": 70,
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

if sys.argv[1] in conf:
	conf = conf[sys.argv[1]]
else:
	sys.exit()

####################
# INIT
####################

output_dir = f"output/{datetime.date.today().strftime('%Y-%m-%d')}"

if not os.path.exists(output_dir):
	os.mkdir(output_dir)

video_width = conf["format"][0]
video_height = conf["format"][1]

video_name = f'{output_dir}/highlite_{sys.argv[1]}_{datetime.date.today().strftime("%Y-%m-%d")}.avi'
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter(video_name, fourcc, 24, (video_width, video_height))

color_yellow = (243, 242, 121)
color_dark_yellow = (255, 204, 64)
color_blue = (151, 242, 243)
color_dark_blue = (55, 196, 255)  

color_bgr_yellow = (151, 242, 243)
color_bgr_dark_yellow = (64, 204, 255)
color_bgr_blue = (243, 242, 151)
color_bgr_dark_blue = (255, 196, 55)

category = "COVID-19"

# Select the articles

articles = json.load(open(os.path.join("data", datetime.date.today().strftime("%Y-%m-%d"), "0_filtered_articles.json"), "r"))

####################
# CREATE DEFAULT FRAME
####################

img_background = cv2.imread('static/img/background/background-covid.jpg', -1)
if conf["format"][0] > len(img_background[0]) or conf["format"][1] > len(img_background):
	img_background = resize_image(img_background, 2)
img_background = crop_image_in_center(img_background, video_width, video_height)
img_logo = cv2.imread('static/img/logo/Highlite125x400.png', -1)

default_frame = apply_dark_effect(img_background)
default_frame = overlay_highlight_frame(img_background)
default_frame = overlay_image(default_frame, img_logo, (50, 50))

today = datetime.date.today().strftime("%d-%m-%Y")

# Add the circles

circle_positions = []

for i in range(0, len(articles)):
	default_frame = cv2.circle(default_frame, conf["circle"]["pos"](i, len(articles)), conf["circle"]["size"], color_bgr_yellow, -1)

####################
# GENERATE THE INTRO
####################

image_intro = copy.copy(default_frame)

font = ImageFont.truetype("static/font/bungee/Bungee-Regular.otf", 300)
img_pil = Image.fromarray(default_frame)
draw = ImageDraw.Draw(img_pil)
w, h = draw.textsize(category, font=font)
txt = f"Les {len(articles)} articles du jour sur"

for n in range(4 * 24):
	#image_intro = overlay_text(default_frame, txt, (int(video_width / 2) - int(w / 2) + 20, 380), 70, color_bgr_dark_yellow, f=n)
	image_intro = overlay_text(default_frame, txt, conf["title2"]["pos"], conf["title2"]["size"], color_bgr_dark_yellow, f=n)
	image_intro = overlay_text(image_intro, category, conf["title1"]["pos"], conf["title1"]["size"], color_bgr_dark_yellow, f=n)
	image_intro = overlay_text(image_intro, today, conf["intro_date"]["pos"], conf["intro_date"]["size"], color_bgr_blue, pos_type="right", f=n)
	video.write(image_intro)

####################
# GENERATE ARTICLES
####################

frame = copy.copy(default_frame)

frame = overlay_text(frame, "COVID-19", conf["theme"]["pos"], conf["theme"]["size"], color_bgr_dark_yellow, pos_type="right")
frame = overlay_text(frame, today, conf["date"]["pos"], conf["date"]["size"], color_bgr_blue, pos_type="right")

images_splash = read_webp('static/img/splash1.webp')

# Generate for each article
	
for i, article in enumerate(articles):

	frame_article = cv2.circle(frame, conf["circle"]["pos"](i, len(articles)), conf["circle"]["size"], color_bgr_blue, -1)
	default_frame = cv2.circle(default_frame, conf["circle"]["pos"](i, len(articles)), conf["circle"]["size"], color_bgr_blue, -1)

	image_logo = cv2.imread(article["image"], -1)
	
	if image_logo is not None:
		
		for y, _ in enumerate(range(5 * 24)):
			frame_a = copy.copy(frame_article)

			# Add the content

			frame_a = overlay_text(frame_a, article["title"], conf["article"]["title_pos"], conf["article"]["font_size"], color_bgr_blue, max_width=conf["article"]["title_max_width"], f=y)
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

image_twitter = cv2.imread("static/img/social-network/twitter512x512.png", cv2.IMREAD_UNCHANGED)
image_twitter = resize_image(image_twitter, 0.25)
image_tiktok = cv2.imread("static/img/social-network/tiktok512x512.png", cv2.IMREAD_UNCHANGED)
image_tiktok = resize_image(image_tiktok, 0.25)
image_instagram = cv2.imread("static/img/social-network/instagram512x512.png", cv2.IMREAD_UNCHANGED)
image_instagram = resize_image(image_instagram, 0.25)
image_snapchat = cv2.imread("static/img/social-network/snapchat128x128.png", cv2.IMREAD_UNCHANGED)

pos_el1 = int(video_width / 2 - 600)
pos_el2 = int(video_width / 2 - 200)
pos_el3 = int(video_width / 2 + 200)
pos_el4 = int(video_width / 2 + 600)

for y, _ in enumerate(range(6 * 24)):
	txt = "Thanks for watching..."
	frame = overlay_text(default_frame, txt, conf["date"]["pos"], conf["date"]["size"], color_bgr_blue, pos_type="right", f=max(0, y))
	txt = "Nouvelle vidéo COVID-19 tous les jours à 19h"
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

"""my_clip = mpe.VideoFileClip('./video.avi')
audio_background = mpe.AudioFileClip('./sound/Coupe.mp4')
final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(final_audio)"""

####################
# CONVERT TO MP4
####################

current_path = pathlib.Path(__file__).parent.absolute()

'''process = (
	ffmpeg
	.input(os.path.join(current_path, video_name).replace("/", "\\"))
	#.output(os.path.join(current_path, video_name[:-4] + ".mp4").replace("\\", "/"), format="mp4")
	.output("pipe:", format="mp4")
	.run_async(pipe_stdout=True)
)
out, err = process.communicate()
print(out, err)'''

'''print(os.path.join(current_path, video_name).replace("\\", "/"))
print(os.path.join(current_path, video_name[:-4] + ".mp4").replace("\\", "/"))

input = ffmpeg.input(video_name.split("/")[-1])
output = ffmpeg.output(input, os.path.join(current_path, video_name[:-4] + ".mp4").replace("\\", "/"), format="mp4")
output.run()'''

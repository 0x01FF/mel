import cv2
import pygame as pg
from math import ceil
from PIL import Image
DIE_WIDTH = 25
RESOLUTION_FACTOR = 2
DOT_CENTERS = {
    1: [(0, 0)],
    2: [(1, -1), (-1, 1)],
    3: [(1, -1), (0, 0), (-1, 1)],
    4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    5: [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)],
    6: [(-1, -1), (1, -1), (-1, 1), (1, 1), (-1, 0), (1, 0)]
}
def convert_dice(image_path):
	if image_path[-3:] != "png":
		im1 = Image.open(image_path)
		image_path = image_path[:-3]+"png"
		im1.save(image_path)
	pg.init()
	img = cv2.imread(image_path, 0)
	HEIGHT, WIDTH = img.shape
	WIDTH *= RESOLUTION_FACTOR
	HEIGHT *= RESOLUTION_FACTOR
	DOT_RADIUS = DIE_WIDTH // 25
	GRID_WIDTH = WIDTH // DIE_WIDTH
	GRID_HEIGHT = HEIGHT // DIE_WIDTH
	w = pg.display.set_mode((GRID_WIDTH * DIE_WIDTH, GRID_HEIGHT * DIE_WIDTH))
	img = cv2.resize(img, (GRID_WIDTH, GRID_HEIGHT), interpolation=cv2.INTER_AREA)
	for pixel_x in range(GRID_WIDTH):
		for pixel_y in range(GRID_HEIGHT):
			brightness = img[pixel_y][pixel_x]
			die_number = ceil(brightness / 42.5)  # Map to 1-6
			if die_number == 0:
				continue
			die_x = pixel_x*DIE_WIDTH + 0.5*DIE_WIDTH
			die_y = pixel_y*DIE_WIDTH + 0.5*DIE_WIDTH
			for dotCenter in DOT_CENTERS[die_number]:
				dot_x = die_x + dotCenter[0]*DIE_WIDTH*0.25
				dot_y = die_y + dotCenter[1]*DIE_WIDTH*0.25
				pg.draw.circle(w, [255, 255, 255], (int(dot_x), int(dot_y)), DOT_RADIUS)
	for i in range(GRID_WIDTH):
		x = i * DIE_WIDTH
		pg.draw.line(w, [50, 50, 50], (x, 0), (x, HEIGHT))
	for i in range(GRID_HEIGHT):
		y = i * DIE_WIDTH
		pg.draw.line(w, [50, 50, 50], (0, y), (WIDTH, y))
	pg.display.update()
	pg.image.save(w, image_path[:-4]+"_dice.png")
	pg.quit()

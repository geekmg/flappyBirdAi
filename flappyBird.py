import sys
from FlappyBird.Bird import Bird
from FlappyBird.Pipe import Pipe

import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 160 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
SCORE = 0

BACKGROUND = pygame.image.load('./assets/bg.png')




def game():

	

	pygame.init()

	FPSCLOCK = pygame.time.Clock()
	DISPLAY  = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption('Flappy Bird')

	global SCORE

	bird = Bird(DISPLAY, SCREENWIDTH, SCREENHEIGHT)
	pipe1 = Pipe(DISPLAY, SCREENWIDTH+100, PIPEGAPSIZE, SCREENWIDTH)
	pipe2 = Pipe(DISPLAY, SCREENWIDTH+100+(SCREENWIDTH/2), PIPEGAPSIZE, SCREENWIDTH)

	pipeGroup = pygame.sprite.Group()
	pipeGroup.add(pipe1.upperBlock)
	pipeGroup.add(pipe2.upperBlock)
	pipeGroup.add(pipe1.lowerBlock)
	pipeGroup.add(pipe2.lowerBlock)

	moved = False
	pause =0

	while True:

		DISPLAY.blit(BACKGROUND,(0,0))

		t = pygame.sprite.spritecollideany(bird,pipeGroup)

		if t!=None or (bird.y== 512 - bird.height) or (bird.y == 0):
			print("GAME OVER")
			print("FINAL SCORE IS %d"%SCORE)
			return(SCORE)
			

		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE )):
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_RETURN):
				bird.move("UP")
				moved = True
			if event.type == KEYDOWN and event.key == K_m :
				pause=1
		

		if moved == False:
			bird.move(None)
		else:
			moved = False

		
		pipe1Pos = pipe1.move()
		if pipe1Pos[0] <= int(SCREENWIDTH * 0.2) - int(bird.rect.width/2):
			if pipe1.behindBird == 0:
				pipe1.behindBird = 1
				SCORE += 1
				print("SCORE IS %d"%SCORE)

		pipe2Pos = pipe2.move()
		if pipe2Pos[0] <= int(SCREENWIDTH * 0.2) - int(bird.rect.width/2):
			if pipe2.behindBird == 0:
				pipe2.behindBird = 1
				SCORE += 1
				print("SCORE IS %d"%SCORE)
		
		

		if pause==0:
			pygame.display.update()

		FPSCLOCK.tick(FPS)

game()


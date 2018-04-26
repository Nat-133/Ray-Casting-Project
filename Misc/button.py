import pygame
from pygame.locals import *

class Button:

	def __init__(self,screen, nextState, nextStateArgs, text,textSize,primaryColour,secondaryColour,centrePos):
		self.screen = screen
		screenWidth,screenHeight = self.screen.get_size()

		self.nextState = nextState
		self.nextStateArgs = nextStateArgs
		self.font = pygame.font.Font(None, textSize)
		self.primaryColour = primaryColour
		self.secondaryColour = secondaryColour
		self.defaultText = self.font.render(text, True, self.secondaryColour)
		self.secondaryText = self.font.render(text, True, self.primaryColour)
		self.rect = self.defaultText.get_rect(center=(int(screenWidth/2)+centrePos[0],int(screenHeight/2)+centrePos[1]))

	def draw(self,mousePos):
		if self.rect.collidepoint(mousePos):
			pygame.draw.rect(self.screen,self.secondaryColour,self.rect)
			self.screen.blit(self.secondaryText,self.rect)
		else:
			pygame.draw.rect(self.screen,self.primaryColour,self.rect)
			self.screen.blit(self.defaultText,self.rect)

	def isClicked(self,mousePos):
		if self.rect.collidepoint(mousePos):
			return True
		else:
			return False


import pygame as pg
import requests
from urllib.parse import unquote
import random as rd
import html
from data import data
class Spritesheet:
 
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self,x,y,width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        return image

def get_question_pool():
    results =  data["results"]
    return results

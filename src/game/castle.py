import pygame
from .unit import Unit
import random

class Castle:
    def __init__(self, screen, position, team):
        self.screen = screen
        self.position = position
        self.team = team
        self.gold = 0
        self.health = 100

    def draw(self):
        # 성 그리기
        if self.position == "left":
            pygame.draw.rect(self.screen, (128, 128, 128), (0, 0, 100, 600))
        else:
            pygame.draw.rect(self.screen, (128, 128, 128), (700, 0, 100, 600))
            
        # 골드 표시
        font = pygame.font.SysFont(None, 36)
        gold_text = font.render(f"Gold: {self.gold}", True, (255, 215, 0))
        
        if self.position == "left":
            gold_rect = gold_text.get_rect(topleft=(10, 510))
        else:
            gold_rect = gold_text.get_rect(topright=(790, 510))
            
        self.screen.blit(gold_text, gold_rect) 
import pygame
import random

class Unit:
    def __init__(self, screen, position, unit_type):
        self.screen = screen
        self.position = position
        self.unit_type = unit_type
        
        # 유닛 타입별 속성 설정
        if unit_type == "전사":
            self.cost = 100
            self.attack = 10
            self.health = 100
            self.speed = 5
            self.color = (200, 50, 50)
            self.size = 20
        elif unit_type == "궁수":
            self.cost = 150
            self.attack = 15
            self.health = 80
            self.speed = 3
            self.color = (50, 200, 50)
            self.size = 15
        elif unit_type == "기사":
            self.cost = 200
            self.attack = 20
            self.health = 150
            self.speed = 2
            self.color = (50, 50, 200)
            self.size = 25
            
        # 초기 위치 설정 (성 바로 앞에서 시작)
        screen_height = 1080
        castle_height = int(screen_height * 0.2)  # 성의 높이 (20%)
        
        self.y = screen_height - castle_height - self.size  # 성 위에서 시작
        
        if position == "left":
            self.x = int(1920 * 0.2) + self.size  # 왼쪽 성 오른쪽 끝에서 시작
        else:
            self.x = 1920 - int(1920 * 0.2) - self.size  # 오른쪽 성 왼쪽 끝에서 시작
        
    def move(self):
        # 왼쪽 유닛은 오른쪽으로, 오른쪽 유닛은 왼쪽으로 이동
        if self.position == "left":
            self.x += self.speed
        else:
            self.x -= self.speed
            
    def draw(self):
        # 유닛 그리기
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size)
        
        # 체력바 그리기
        health_width = 40
        health_height = 5
        health_x = self.x - health_width//2
        health_y = self.y - self.size - 10
        
        # 체력바 배경
        pygame.draw.rect(self.screen, (200, 0, 0),
                        (health_x, health_y, health_width, health_height))
        # 현재 체력
        current_health_width = int(health_width * (self.health / 100))
        pygame.draw.rect(self.screen, (0, 200, 0),
                        (health_x, health_y, current_health_width, health_height))
                        
    def is_dead(self):
        return self.health <= 0
        
    def take_damage(self, damage):
        self.health -= damage
        return self.is_dead() 
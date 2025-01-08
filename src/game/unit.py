import pygame
import random

class Unit:
    def __init__(self, screen, position, unit_type):
        self.screen = screen
        self.position = position
        self.unit_type = unit_type
        
        # ��면 크기
        self.screen_width = 1920
        self.screen_height = 1080
        self.castle_height = int(self.screen_height * 0.2)
        
        # 유닛 타입별 속성 설정
        if unit_type == "전사":
            self.cost = 100
            self.attack = 10
            self.health = 100
            self.speed = 3
            self.color = (200, 50, 50)
            self.size = 15
        elif unit_type == "궁수":
            self.cost = 150
            self.attack = 15
            self.health = 80
            self.speed = 2
            self.color = (50, 200, 50)
            self.size = 12
        elif unit_type == "기사":
            self.cost = 200
            self.attack = 20
            self.health = 150
            self.speed = 1
            self.color = (50, 50, 200)
            self.size = 18
            
        # 초기 위치 설정 (성 앞에서 시작)
        self.y = self.screen_height - self.castle_height - self.size
        
        if position == "left":
            self.x = int(self.screen_width * 0.2)  # 왼쪽 성 오른쪽 끝
        else:
            self.x = int(self.screen_width * 0.8)  # 오른쪽 성 왼쪽 끝
            
        # 약간의 랜덤 위치 추가 (유닛 겹침 방지)
        self.y += random.randint(-30, 30)
        
    def move(self):
        # 왼쪽 유닛은 오른쪽으로, 오른쪽 유닛은 왼쪽으로 이동
        if self.position == "left":
            self.x += self.speed
        else:
            self.x -= self.speed
            
    def draw(self):
        # 유닛 그리기
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size)
        
        # 체력바 그리기
        health_width = self.size * 2
        health_height = 4
        health_x = self.x - health_width//2
        health_y = self.y - self.size - 8
        
        # 체력바 배경
        pygame.draw.rect(self.screen, (200, 0, 0),
                        (health_x, health_y, health_width, health_height))
        # 현재 체력
        current_health = int(health_width * (self.health / 100))
        pygame.draw.rect(self.screen, (0, 200, 0),
                        (health_x, health_y, current_health, health_height))
                        
    def is_dead(self):
        return self.health <= 0
        
    def take_damage(self, damage):
        self.health -= damage
        return self.is_dead()
        
    def check_collision(self, other):
        # 두 유닛 사이의 거리 계산
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return distance < (self.size + other.size) 
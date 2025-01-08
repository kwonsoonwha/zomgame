import pygame

class Unit:
    def __init__(self, x, y, team, unit_type):
        self.x = x
        self.y = y
        self.team = team
        self.unit_type = unit_type
        self.size = 30
        
        # 기본 속도를 80% 감소
        self.base_speed = 0.4  # 원래 2.0이었던 것을 0.4로 조정
        
        # 유닛 타입별 스탯
        if unit_type == 'warrior':
            self.speed = self.base_speed
            self.health = 100
            self.attack = 10
            self.cost = 100
            self.color = (200, 0, 0) if team == 'left' else (0, 0, 200)
        elif unit_type == 'archer':
            self.speed = self.base_speed * 0.75
            self.health = 70
            self.attack = 15
            self.cost = 150
            self.color = (150, 0, 0) if team == 'left' else (0, 0, 150)
        elif unit_type == 'knight':
            self.speed = self.base_speed * 0.5
            self.health = 150
            self.attack = 20
            self.cost = 200
            self.color = (250, 0, 0) if team == 'left' else (0, 0, 250)
            
    def move(self):
        if self.team == 'left':
            self.x += self.speed
        else:
            self.x -= self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        # 체력바 그리기
        health_ratio = self.health / (100 if self.unit_type == 'warrior' else 70 if self.unit_type == 'archer' else 150)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, self.size * health_ratio, 5))

    def attack_unit(self, target):
        target.health -= self.attack
        return target.health <= 0 
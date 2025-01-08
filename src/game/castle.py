import pygame
from .unit import Unit

class Castle:
    def __init__(self, screen, position, team):
        self.screen = screen
        self.position = position
        self.team = team
        self.gold = 0
        self.health = 100
        
        # 화면 크기의 20%를 성의 크기로 설정
        screen_width = 1920
        screen_height = 1080
        self.castle_width = int(screen_width * 0.2)  # 화면 너비의 20%
        self.castle_height = int(screen_height * 0.2)  # 화면 높이의 20%
        
        # 성의 위치 설정 (하단에 배치)
        self.castle_y = screen_height - self.castle_height
        if position == "left":
            self.castle_x = 0
        else:
            self.castle_x = screen_width - self.castle_width
        
        # 유닛 생산 버튼 위치 재설정
        button_width = 150
        button_height = 40
        button_margin = 10
        button_start_y = self.castle_y + 30
        
        self.unit_buttons = [
            {"type": "전사", "cost": 100, "rect": pygame.Rect(
                self.castle_x + (self.castle_width - button_width)//2,
                button_start_y,
                button_width, button_height)},
            {"type": "궁수", "cost": 150, "rect": pygame.Rect(
                self.castle_x + (self.castle_width - button_width)//2,
                button_start_y + button_height + button_margin,
                button_width, button_height)},
            {"type": "기사", "cost": 200, "rect": pygame.Rect(
                self.castle_x + (self.castle_width - button_width)//2,
                button_start_y + (button_height + button_margin)*2,
                button_width, button_height)}
        ]
        
    def draw(self):
        # 성 그리기 (하단 20% 크기)
        castle_color = (128, 128, 128)
        pygame.draw.rect(self.screen, castle_color, 
                        (self.castle_x, self.castle_y, 
                         self.castle_width, self.castle_height))
            
        # 체력바 그리기
        health_width = int(self.castle_width * 0.8)
        health_height = 20
        health_x = self.castle_x + (self.castle_width - health_width)//2
        health_y = self.castle_y + 10
        
        # 체력바 배경
        pygame.draw.rect(self.screen, (200, 0, 0), 
                        (health_x, health_y, health_width, health_height))
        # 현재 체력
        current_health_width = int(health_width * (self.health / 100))
        pygame.draw.rect(self.screen, (0, 200, 0),
                        (health_x, health_y, current_health_width, health_height))
            
        # 유닛 생산 버튼 그리기
        font = pygame.font.SysFont('malgungothic', 24)  # 폰트 크기 조정
        for button in self.unit_buttons:
            # 버튼 배경
            color = (200, 200, 200) if self.gold >= button["cost"] else (150, 150, 150)
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, (100, 100, 100), button["rect"], 2)
            
            # 유닛 정보 텍스트
            unit_text = f"{button['type']}: {button['cost']}"
            text = font.render(unit_text, True, (0, 0, 0))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
            
        # 골드 표시
        gold_font = pygame.font.SysFont('malgungothic', 32)
        gold_text = gold_font.render(f"Gold: {self.gold}", True, (255, 215, 0))
        gold_y = self.castle_y + self.castle_height - 40
        if self.position == "left":
            gold_rect = gold_text.get_rect(left=self.castle_x + 10, top=gold_y)
        else:
            gold_rect = gold_text.get_rect(right=self.castle_x + self.castle_width - 10, 
                                         top=gold_y)
        self.screen.blit(gold_text, gold_rect)
        
    def create_unit(self, unit_type):
        # 유닛 생성 비용 확인
        for button in self.unit_buttons:
            if button["type"] == unit_type and self.gold >= button["cost"]:
                self.gold -= button["cost"]
                return Unit(self.screen, self.position, unit_type)
        return None
        
    def check_unit_click(self, pos):
        # 유닛 생산 버튼 클릭 체크
        for button in self.unit_buttons:
            if button["rect"].collidepoint(pos) and self.gold >= button["cost"]:
                return button["type"]
        return None
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0 
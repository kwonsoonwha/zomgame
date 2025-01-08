import pygame
from .unit import Unit

class Castle:
    def __init__(self, screen, position, team):
        self.screen = screen
        self.position = position
        self.team = team
        self.gold = 1000  # ��기 골드 설정
        self.health = 100
        
        # 화면 크기 계산
        self.screen_width = 1920
        self.screen_height = 1080
        
        # 성의 크기 (화면 높이의 20%)
        self.castle_height = int(self.screen_height * 0.2)
        self.castle_width = int(self.screen_width * 0.2)
        
        # 성의 위치 (하단에 배치)
        self.castle_y = self.screen_height - self.castle_height
        if position == "left":
            self.castle_x = 0
        else:
            self.castle_x = self.screen_width - self.castle_width
            
        # 유닛 생산 버튼 설정
        button_width = 120
        button_height = 40
        button_margin = 10
        button_start_y = self.castle_y + 20
        
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
        # 성 그리기
        castle_color = (100, 100, 100)
        pygame.draw.rect(self.screen, castle_color,
                        (self.castle_x, self.castle_y,
                         self.castle_width, self.castle_height))
                         
        # 체력바 그리기
        health_width = int(self.castle_width * 0.8)
        health_height = 15
        health_x = self.castle_x + (self.castle_width - health_width)//2
        health_y = self.castle_y + 10
        
        # 체력바 배경
        pygame.draw.rect(self.screen, (200, 0, 0),
                        (health_x, health_y, health_width, health_height))
        # 현재 체력
        current_health = int(health_width * (self.health / 100))
        pygame.draw.rect(self.screen, (0, 200, 0),
                        (health_x, health_y, current_health, health_height))
                        
        # 유닛 생산 버튼 그리기
        font = pygame.font.SysFont('malgungothic', 20)
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
        gold_font = pygame.font.SysFont('malgungothic', 24)
        gold_text = gold_font.render(f"Gold: {self.gold}", True, (255, 215, 0))
        if self.position == "left":
            gold_rect = gold_text.get_rect(
                left=self.castle_x + 10,
                bottom=self.castle_y + self.castle_height - 10)
        else:
            gold_rect = gold_text.get_rect(
                right=self.castle_x + self.castle_width - 10,
                bottom=self.castle_y + self.castle_height - 10)
        self.screen.blit(gold_text, gold_rect)
        
    def create_unit(self, unit_type):
        return Unit(self.screen, self.position, unit_type)
        
    def check_unit_click(self, pos):
        for button in self.unit_buttons:
            if button["rect"].collidepoint(pos):
                if self.gold >= button["cost"]:
                    self.gold -= button["cost"]
                    return button["type"]
        return None
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0 
        
    def add_gold(self, amount):
        if amount > 0:  # 양수일 때만 추가
            self.gold += amount

    def remove_gold(self, amount):
        if amount > 0 and self.gold >= amount:  # 양수이고 충분한 골드가 있을 때만
            self.gold -= amount
            return True
        return False

    def set_gold(self, amount):  # 골드 직접 설정 (디버깅용)
        self.gold = max(0, amount)  # 음수 방지 
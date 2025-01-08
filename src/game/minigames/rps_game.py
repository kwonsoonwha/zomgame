import pygame
import random

class RPSGame:
    def __init__(self, screen):
        self.screen = screen
        self.choices = ['가위', '바위', '보']
        self.player_choice = None
        self.computer_choice = None
        self.bet_amount = 100
        self.min_bet = 100
        self.result = None
        self.result_timer = 0
        
        # 폰트 설정
        self.font = pygame.font.SysFont('malgungothic', 72)
        self.small_font = pygame.font.SysFont('malgungothic', 36)
        self.title_font = pygame.font.SysFont('malgungothic', 48)
        
        # 위치 계산 (왼쪽 중앙)
        self.x = 400
        self.y = 200
        
    def draw(self):
        # 메인 패널
        panel_width = 400
        panel_height = 500
        pygame.draw.rect(self.screen, (160, 160, 160), 
                        (self.x, self.y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (self.x+5, self.y+5, panel_width-10, panel_height-10))
        
        # 제목
        title = self.title_font.render("가위바위보", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.x + panel_width//2, self.y + 40))
        self.screen.blit(title, title_rect)
        
        # 선택 버튼
        for i, choice in enumerate(self.choices):
            # 버튼 배경
            color = (180, 180, 180) if self.player_choice == choice else (220, 220, 220)
            pygame.draw.rect(self.screen, color, 
                           (self.x + 30 + i*125, self.y + 100, 115, 100))
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (self.x + 30 + i*125, self.y + 100, 115, 100), 2)
            
            # 버튼 텍스트
            text = self.font.render(choice, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + 87 + i*125, self.y + 150))
            self.screen.blit(text, text_rect)
        
        # 결과 표시
        if self.result:
            result_colors = {
                "승리": (50, 200, 50),
                "패배": (200, 50, 50),
                "무승부": (100, 100, 100)
            }
            color = result_colors.get(self.result, (0, 0, 0))
            
            # 컴퓨터 선택
            comp_text = self.title_font.render(f"컴퓨터: {self.computer_choice}", True, (0, 0, 0))
            comp_rect = comp_text.get_rect(center=(self.x + panel_width//2, self.y + 250))
            self.screen.blit(comp_text, comp_rect)
            
            # 결과
            result_text = self.title_font.render(self.result, True, color)
            result_rect = result_text.get_rect(center=(self.x + panel_width//2, self.y + 300))
            self.screen.blit(result_text, result_rect)
        
        # 베팅 컨트롤
        pygame.draw.rect(self.screen, (40, 40, 40), 
                        (self.x + 50, self.y + 400, 300, 40))
        bet_text = self.title_font.render(f"베팅: {self.bet_amount}", True, (0, 255, 0))
        bet_rect = bet_text.get_rect(center=(self.x + 200, self.y + 420))
        self.screen.blit(bet_text, bet_rect)
        
        # 베팅 버튼
        for i, (text, x) in enumerate([("-", self.x + 20), ("+", self.x + 330)]):
            pygame.draw.rect(self.screen, (200, 200, 200), (x, self.y + 400, 40, 40))
            btn_text = self.font.render(text, True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=(x + 20, self.y + 420))
            self.screen.blit(btn_text, btn_rect)
            
    def play(self, choice):
        if not self.result:
            self.player_choice = choice
            self.computer_choice = random.choice(self.choices)
            
            # 승패 판정
            if self.player_choice == self.computer_choice:
                self.result = "무승부"
                return 0
            elif ((self.player_choice == "가위" and self.computer_choice == "보") or
                  (self.player_choice == "바위" and self.computer_choice == "가위") or
                  (self.player_choice == "보" and self.computer_choice == "바위")):
                self.result = "승리"
                return self.bet_amount * 2
            else:
                self.result = "패배"
                return -self.bet_amount
        return 0
        
    def change_bet(self, increase):
        if increase:
            self.bet_amount += 100
        else:
            self.bet_amount = max(self.min_bet, self.bet_amount - 100) 
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
        self.max_bet = 500
        self.result = None
        self.result_timer = 0
        
        # 폰트 �정
        try:
            font_path = "assets/fonts/NanumGothic.ttf"
            self.font = pygame.font.Font(font_path, 36)
            self.small_font = pygame.font.Font(font_path, 24)
            self.title_font = pygame.font.Font(font_path, 28)
        except:
            print("폰트 로드 실패, 시스템 폰트 사용")
            self.font = pygame.font.SysFont('malgungothic', 36)
            self.small_font = pygame.font.SysFont('malgungothic', 24)
            self.title_font = pygame.font.SysFont('malgungothic', 28)
        
    def make_choice(self, choice):
        if self.result_timer <= 0:
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
                self.result_timer = 120
                return self.bet_amount
            else:
                self.result = "패배"
                self.result_timer = 120
                return -self.bet_amount
        return 0
        
    def update(self):
        if self.result_timer > 0:
            self.result_timer -= 1
            if self.result_timer <= 0:
                self.reset()  # 타이머가 끝나면 리셋
    
    def reset(self):
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.result_timer = 0
    
    def change_bet(self, increase):
        if increase:
            self.bet_amount = min(self.max_bet, self.bet_amount + 100)
        else:
            self.bet_amount = max(self.min_bet, self.bet_amount - 100)
    
    def draw(self):
        # 메� 패널
        pygame.draw.rect(self.screen, (160, 160, 160), (20, 150, 300, 360))
        pygame.draw.rect(self.screen, (200, 200, 200), (25, 155, 290, 350))
        
        # 제목
        title = self.title_font.render("가위바위보", True, (0, 0, 0))
        title_rect = title.get_rect(center=(170, 185))
        self.screen.blit(title, title_rect)
        
        # 선택 버튼
        for i, choice in enumerate(self.choices):
            # 버튼 배경
            color = (220, 220, 220) if self.player_choice != choice else (180, 180, 180)
            pygame.draw.rect(self.screen, color, (40 + i*95, 220, 85, 80))
            pygame.draw.rect(self.screen, (100, 100, 100), (40 + i*95, 220, 85, 80), 1)
            
            # 버튼 텍스트
            text = self.font.render(choice, True, (0, 0, 0))
            text_rect = text.get_rect(center=(82 + i*95, 260))
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
            comp_rect = comp_text.get_rect(center=(170, 320))
            self.screen.blit(comp_text, comp_rect)
            
            # 결과
            result_text = self.title_font.render(self.result, True, color)
            result_rect = result_text.get_rect(center=(170, 360))
            self.screen.blit(result_text, result_rect)
        
        # 베팅 컨트롤
        pygame.draw.rect(self.screen, (220, 220, 220), (40, 400, 260, 80))
        
        # 베팅 버튼
        for i, (text, x) in enumerate([("-", 50), ("+", 260)]):
            pygame.draw.rect(self.screen, (200, 200, 200), (x, 420, 35, 35))
            pygame.draw.rect(self.screen, (100, 100, 100), (x, 420, 35, 35), 1)
            btn_text = self.font.render(text, True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=(x + 17, 437))
            self.screen.blit(btn_text, btn_rect)
        
        # 베팅 금액
        bet_text = self.title_font.render(f"베팅: {self.bet_amount}", True, (0, 0, 0))
        bet_rect = bet_text.get_rect(center=(170, 437))
        self.screen.blit(bet_text, bet_rect) 
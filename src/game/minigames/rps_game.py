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
        self.win_amount = 0
        
        # 폰트 설정
        self.font = pygame.font.SysFont('malgungothic', 36)
        self.small_font = pygame.font.SysFont('malgungothic', 24)
        self.title_font = pygame.font.SysFont('malgungothic', 48)
        
        # 위치 계산 (화면 중앙 상단, 슬롯머신 옆)
        self.x = 960 + 220  # 슬롯머신 오른쪽에 배치
        self.y = 50  # 상단에 배치
        
    def draw(self):
        # 패널 크기
        panel_width = 400
        panel_height = 300
        
        # 메인 패널
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (self.x, self.y, panel_width, panel_height))
        
        # 제목
        title = self.title_font.render("가위바위보", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.x + panel_width//2, self.y + 30))
        self.screen.blit(title, title_rect)
        
        # 선택 버튼
        for i, choice in enumerate(self.choices):
            button_color = (150, 150, 150)
            if self.player_choice == choice:
                button_color = (100, 200, 100)
            
            pygame.draw.rect(self.screen, button_color,
                           (self.x + 50 + i*120, self.y + 70, 100, 50))
            
            choice_text = self.font.render(choice, True, (0, 0, 0))
            choice_rect = choice_text.get_rect(
                center=(self.x + 100 + i*120, self.y + 95))
            self.screen.blit(choice_text, choice_rect)
        
        # 결과 표시
        if self.result:
            result_color = {
                "승리": (0, 255, 0),
                "패배": (255, 0, 0),
                "무승부": (255, 255, 0)
            }.get(self.result, (255, 255, 255))
            
            # 컴퓨터의 선택
            comp_text = self.font.render(f"컴퓨터: {self.computer_choice}", 
                                       True, (0, 0, 0))
            comp_rect = comp_text.get_rect(
                center=(self.x + panel_width//2, self.y + 150))
            self.screen.blit(comp_text, comp_rect)
            
            # 결과
            result_text = self.font.render(self.result, True, result_color)
            result_rect = result_text.get_rect(
                center=(self.x + panel_width//2, self.y + 200))
            self.screen.blit(result_text, result_rect)
        
        # 배팅 금액
        bet_text = self.font.render(f"BET: {self.bet_amount}", True, (0, 255, 0))
        bet_rect = bet_text.get_rect(center=(self.x + panel_width//2, self.y + 260))
        self.screen.blit(bet_text, bet_rect)
        
        # 배팅 버튼
        for i, (text, x) in enumerate([("-", self.x + 20), ("+", self.x + 330)]):
            pygame.draw.rect(self.screen, (200, 200, 200), (x, self.y + 240, 40, 40))
            btn_text = self.font.render(text, True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=(x + 20, self.y + 260))
            self.screen.blit(btn_text, btn_rect)
            
    def handle_click(self, pos):
        x, y = pos
        
        # 베팅 버튼 (-/+)
        if self.y + 240 <= y <= self.y + 280:
            if self.x + 20 <= x <= self.x + 60:  # - 버튼
                self.bet_amount = max(self.min_bet, self.bet_amount - 50)
                print("RPS bet decreased:", self.bet_amount)  # 디버깅용
                return True
            elif self.x + 330 <= x <= self.x + 370:  # + 버튼
                self.bet_amount = min(1000, self.bet_amount + 50)
                print("RPS bet increased:", self.bet_amount)  # 디버깅용
                return True
        
        # 가위바위보 선택
        if self.y + 70 <= y <= self.y + 120:
            for i, choice in enumerate(self.choices):
                button_x = self.x + 50 + i*120
                if button_x <= x <= button_x + 100:
                    print(f"Selected {choice}")  # 디��깅용
                    self.play_game(choice)
                    return True
                
        return False

    def play_game(self, choice):
        self.player_choice = choice
        self.computer_choice = random.choice(self.choices)
        
        # 승패 판정
        if self.player_choice == self.computer_choice:
            self.result = "무승부"
        elif ((self.player_choice == "가위" and self.computer_choice == "보") or
              (self.player_choice == "바위" and self.computer_choice == "가위") or
              (self.player_choice == "보" and self.computer_choice == "바위")):
            self.result = "승리"
        else:
            self.result = "패배"

        # 결과에 따른 상금 지급
        if self.result == "승리":
            self.win_amount = self.bet_amount * 2
        elif self.result == "무승부":
            self.win_amount = self.bet_amount
        else:
            self.win_amount = 0

        self.result_timer = pygame.time.get_ticks() 
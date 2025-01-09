import pygame
import random

class RPSGame:
    def __init__(self, screen):
        self.screen = screen
        self.choices = ['가위', '바위', '보']
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.bet_amount = 100
        self.min_bet = 100
        self.game_state = "READY"  # READY, PLAYING, RESULT
        self.result_timer = 0
        
        # 화면 위치 수정 (+150 픽셀)
        screen_width = screen.get_width()
        self.x = (screen_width // 2) + 150  # 오른쪽으로 150픽셀 이동
        self.y = 50
        
    def handle_click(self, pos):
        if self.game_state != "READY":
            return False
            
        x, y = pos
        
        # 베팅 금액 조절 버튼
        if self.y + 240 <= y <= self.y + 280:
            if self.x - 30 <= x <= self.x + 10:  # - 버튼
                self.bet_amount = max(self.min_bet, self.bet_amount - 50)
                return False
            elif self.x + 230 <= x <= self.x + 270:  # + 버튼
                self.bet_amount += 50
                return False
        
        # 가위바위보 선택 영역
        if self.y + 70 <= y <= self.y + 170:
            for i, choice in enumerate(self.choices):
                if self.x + (i-1)*100 - 30 <= x <= self.x + (i-1)*100 + 70:
                    self.player_choice = choice
                    self.computer_choice = random.choice(self.choices)
                    self.game_state = "PLAYING"
                    # 무승부가 아닐 때만 True 반환 (베팅 차감)
                    return self.player_choice != self.computer_choice
        
        return False
        
    def check_result(self):
        if not self.player_choice or not self.computer_choice:
            return 0
            
        if self.player_choice == self.computer_choice:
            self.result = "무승부"
            return 0  # 무승부시 0 반환 (베팅 금액 유지)
            
        winning_combinations = {
            '가위': '보',
            '바위': '가위',
            '보': '바위'
        }
        
        if winning_combinations[self.player_choice] == self.computer_choice:
            self.result = "승리"
            return self.bet_amount * 2  # 승리시 2배
        else:
            self.result = "패배"
            return -self.bet_amount  # 패배시 베팅액 잃음
            
    def update(self):
        if self.game_state == "PLAYING":
            self.game_state = "RESULT"
            self.result_timer = pygame.time.get_ticks()
            return self.check_result()
            
        elif self.game_state == "RESULT":
            current_time = pygame.time.get_ticks()
            if current_time - self.result_timer >= 2000:  # 2초 후
                self.game_state = "READY"
                self.player_choice = None
                self.computer_choice = None
                self.result = None
                
        return 0
        
    def draw(self):
        # 메인 패널
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (self.x - 50, self.y, 400, 300))
        
        # 제목
        title_font = pygame.font.SysFont('malgungothic', 36)
        title = title_font.render("가위바위보", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.x + 150, self.y + 30))
        self.screen.blit(title, title_rect)
        
        # 선택 버튼들
        choice_font = pygame.font.SysFont('malgungothic', 48)
        for i, choice in enumerate(self.choices):
            color = (150, 150, 150)
            if self.game_state == "READY":
                color = (200, 200, 200)
            elif self.player_choice == choice:
                color = (100, 255, 100)
                
            pygame.draw.rect(self.screen, color,
                           (self.x + (i-1)*100 - 30, self.y + 70, 100, 100))
            
            text = choice_font.render(choice, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(self.x + (i-1)*100 + 20, self.y + 120))
            self.screen.blit(text, text_rect)
        
        # 결과 표시
        if self.game_state == "RESULT":
            result_text = f"컴퓨터: {self.computer_choice}\n{self.result}"
            result_font = pygame.font.SysFont('malgungothic', 36)
            y_offset = 0
            for line in result_text.split('\n'):
                text = result_font.render(line, True, (255, 0, 0))
                text_rect = text.get_rect(center=(self.x + 150, self.y + 200 + y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 40
        
        # 베팅 금액
        bet_text = title_font.render(f"BET: {self.bet_amount}", True, (0, 255, 0))
        bet_rect = bet_text.get_rect(center=(self.x + 150, self.y + 260))
        self.screen.blit(bet_text, bet_rect)
        
        # 베팅 버튼
        for text, x in [("-", self.x - 30), ("+", self.x + 230)]:
            pygame.draw.rect(self.screen, (200, 200, 200), (x, self.y + 240, 40, 40))
            btn_text = choice_font.render(text, True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=(x + 20, self.y + 260))
            self.screen.blit(btn_text, btn_rect) 
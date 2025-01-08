import pygame
import random
import math

class SlotMachine:
    def __init__(self, screen):
        self.screen = screen
        self.symbols = ['7', 'A', 'K', 'Q', 'J']
        self.reels = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.bet_amount = 100
        self.min_bet = 100
        self.win_amount = 0
        
        # 게임 상태 관리
        self.game_state = "READY"  # READY, SPINNING, PAYING
        self.spin_start_time = 0
        self.spin_duration = 2500  # 총 회전 시간 (ms)
        
        # UI 관련
        screen_width = screen.get_width()
        self.x = (screen_width // 2) - 400
        self.y = 50
        self.error_message = None
        self.error_timer = 0
        
    def handle_click(self, pos, current_gold):
        x, y = pos
        
        # 게임이 진행 중이면 클릭 무시
        if self.game_state != "READY":
            return False
            
        # 베팅 버튼 (-/+)
        if self.y + 240 <= y <= self.y + 280:
            if self.x + 20 <= x <= self.x + 60:  # - 버튼
                self.bet_amount = max(self.min_bet, self.bet_amount - 50)
            elif self.x + 330 <= x <= self.x + 370:  # + 버튼
                self.bet_amount += 50
            return False
        
        # 슬롯 영역 클릭 - 게임 시작
        if (self.x + 50 <= x <= self.x + 350 and 
            self.y + 70 <= y <= self.y + 240):
            if current_gold >= self.bet_amount:
                return True
            else:
                self.show_error("골드가 부족합니다")
                
        return False
        
    def start_spin(self):
        if self.game_state != "READY":
            return
            
        self.game_state = "SPINNING"
        self.spin_start_time = pygame.time.get_ticks()
        self.win_amount = 0
        
        # 최종 결과 결정
        self.final_symbols = [
            [random.randint(0, len(self.symbols)-1) for _ in range(3)],
            [random.randint(0, len(self.symbols)-1) for _ in range(3)],
            [random.randint(0, len(self.symbols)-1) for _ in range(3)]
        ]
        
    def update(self):
        if self.game_state == "READY":
            return
            
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spin_start_time
        
        if self.game_state == "SPINNING":
            # 각 릴 업데이트
            for i in range(3):
                stop_time = (self.spin_duration / 3) * (i + 1)
                if elapsed < stop_time:
                    speed = max(1, (stop_time - elapsed) / 100)
                    for j in range(3):
                        self.reels[i][j] = random.randint(0, len(self.symbols)-1)
                else:
                    for j in range(3):
                        self.reels[i][j] = self.final_symbols[i][j]
            
            # 모든 릴이 정지했는지 확인
            if elapsed >= self.spin_duration:
                self.check_win()
                self.game_state = "PAYING"
                
        elif self.game_state == "PAYING":
            if elapsed >= self.spin_duration + 1000:  # 결과 표시 1초 후
                self.game_state = "READY"
    
    def check_win(self):
        self.win_amount = 0
        seven_lines = 0
        self.winning_lines = []
        
        # 가로줄 체크
        for i in range(3):
            if self.reels[0][i] == self.reels[1][i] == self.reels[2][i]:
                if self.reels[0][i] == 0:  # 777
                    seven_lines += 1
                    self.winning_lines.append(i)
                else:
                    self.winning_lines.append(i)
                    multiplier = 5 - self.reels[0][i]  # A=4배, K=3배, Q=2배, J=1배
                    self.win_amount += self.bet_amount * multiplier
        
        # 777 라인 수에 따른 보상
        if seven_lines == 1:
            self.win_amount += self.bet_amount * 10
        elif seven_lines == 2:
            self.win_amount += self.bet_amount * 500
        elif seven_lines == 3:
            self.win_amount += self.bet_amount * 10000
    
    def draw(self):
        # 메인 패널
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (self.x, self.y, 400, 300))
        
        # 제목
        title_font = pygame.font.SysFont('malgungothic', 36)
        title = title_font.render("SLOT MACHINE", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.x + 200, self.y + 30))
        self.screen.blit(title, title_rect)
        
        # 릴 배경
        for i in range(3):
            pygame.draw.rect(self.screen, (150, 150, 150),
                           (self.x + 50 + i*100, self.y + 70, 80, 180))
            pygame.draw.rect(self.screen, (100, 100, 100),
                           (self.x + 50 + i*100, self.y + 70, 80, 180), 2)
        
        # 심볼 그리기
        symbol_font = pygame.font.SysFont('arial', 48)
        for i in range(3):
            for j in range(3):
                color = (255, 0, 0) if self.symbols[self.reels[i][j]] == '7' else (0, 0, 0)
                symbol = symbol_font.render(self.symbols[self.reels[i][j]], True, color)
                symbol_rect = symbol.get_rect(
                    center=(self.x + 90 + i*100, self.y + 95 + j*60))
                self.screen.blit(symbol, symbol_rect)
        
        # 당첨 라인 표시
        if self.game_state == "PAYING" and pygame.time.get_ticks() % 1000 < 500:
            for line in self.winning_lines:
                pygame.draw.rect(self.screen, (255, 215, 0),
                               (self.x + 50, self.y + 70 + line*60, 300, 50), 3)
        
        # 베팅 금액
        bet_text = title_font.render(f"BET: {self.bet_amount}", True, (0, 255, 0))
        bet_rect = bet_text.get_rect(center=(self.x + 200, self.y + 260))
        self.screen.blit(bet_text, bet_rect)
        
        # 베팅 버튼
        for text, x in [("-", self.x + 20), ("+", self.x + 330)]:
            pygame.draw.rect(self.screen, (200, 200, 200), (x, self.y + 240, 40, 40))
            btn_text = symbol_font.render(text, True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=(x + 20, self.y + 260))
            self.screen.blit(btn_text, btn_rect)
        
        # AUTO SPIN 상태
        auto_color = (200, 50, 50)  # 빨간색 (OFF)
        pygame.draw.rect(self.screen, auto_color, 
                        (self.x, self.y + 300, 400, 40))
        auto_text = title_font.render("AUTO SPIN: OFF", True, (255, 255, 255))
        auto_rect = auto_text.get_rect(center=(self.x + 200, self.y + 320))
        self.screen.blit(auto_text, auto_rect)
        
        # 에러 메시지
        if self.error_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.error_timer < 2000:
                error_font = pygame.font.SysFont('malgungothic', 24)
                error_text = error_font.render(self.error_message, True, (255, 0, 0))
                error_rect = error_text.get_rect(center=(self.x + 200, self.y + 150))
                self.screen.blit(error_text, error_rect)
            else:
                self.error_message = None
        
    def show_error(self, message):
        self.error_message = message
        self.error_timer = pygame.time.get_ticks() 
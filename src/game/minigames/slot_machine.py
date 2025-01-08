import pygame
import random
import math

class SlotMachine:
    def __init__(self, screen):
        self.screen = screen
        self.symbols = ['7', 'A', 'K', 'Q', 'J']
        self.reels = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.spinning = False
        self.bet_amount = 100
        self.min_bet = 100
        self.auto_spin = False
        self.spin_time = 0
        self.win_amount = 0
        self.result_timer = 0
        
        # 폰트 설정
        self.font = pygame.font.SysFont('malgungothic', 72)
        self.small_font = pygame.font.SysFont('malgungothic', 36)
        self.title_font = pygame.font.SysFont('malgungothic', 48)
        
        # 위치 계산 (화면 중앙)
        self.x = 960 - 200  # 중앙 정렬
        self.y = 200
        
    def change_bet(self, increase):
        if increase:
            self.bet_amount += 100
        else:
            self.bet_amount = max(self.min_bet, self.bet_amount - 100)
    
    def spin(self):
        if not self.spinning:
            self.spinning = True
            self.spin_time = 30  # 스핀 시간
            return -self.bet_amount  # 베팅 금액 차감
        return 0
    
    def check_win(self):
        win_amount = 0
        seven_lines = 0  # 777 라인 카운트
        
        # 가로줄 체크
        for row in range(3):
            if all(self.symbols[self.reels[row][col]] == '7' for col in range(3)):
                seven_lines += 1
            elif all(self.symbols[self.reels[row][col]] == self.symbols[self.reels[row][0]] for col in range(3)):
                win_amount += self.bet_amount * 3

        # 대각선 체크
        if all(self.symbols[self.reels[i][i]] == '7' for i in range(3)):
            seven_lines += 1
        elif all(self.symbols[self.reels[i][i]] == self.symbols[self.reels[0][0]] for i in range(3)):
            win_amount += self.bet_amount * 5

        if all(self.symbols[self.reels[i][2-i]] == '7' for i in range(3)):
            seven_lines += 1
        elif all(self.symbols[self.reels[i][2-i]] == self.symbols[self.reels[0][2]] for i in range(3)):
            win_amount += self.bet_amount * 5

        # 777 라인에 따른 보상
        if seven_lines == 1:
            win_amount += self.bet_amount * 10
        elif seven_lines == 2:
            win_amount += self.bet_amount * 200
        elif seven_lines == 3:
            win_amount += self.bet_amount * 5000

        return win_amount
    
    def update(self):
        if self.spinning:
            self.spin_time -= 1
            # 릴 업데이트
            for row in range(3):
                for col in range(3):
                    if self.spin_time > 0:
                        self.reels[row][col] = random.randint(0, len(self.symbols)-1)
            
            if self.spin_time <= 0:
                self.spinning = False
                win = self.check_win()
                self.win_amount = win
                self.result_timer = 120
                
                # 자동 스핀이 켜져 있으면 다시 스핀
                if self.auto_spin and not self.spinning:
                    self.spin()
                
                return win
        return 0
    
    def draw(self):
        # 메� 패널
        panel_width = 400
        panel_height = 600
        pygame.draw.rect(self.screen, (160, 160, 160), 
                        (self.x, self.y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (self.x+5, self.y+5, panel_width-10, panel_height-10))
        
        # 제목
        title = self.title_font.render("SLOT MACHINE", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.x + panel_width//2, self.y + 40))
        self.screen.blit(title, title_rect)
        
        # 릴 그리기
        for row in range(3):
            for col in range(3):
                # 심볼 배경
                pygame.draw.rect(self.screen, (255, 255, 255),
                               (self.x + 50 + col*100, self.y + 100 + row*100, 80, 80))
                # 심볼
                symbol = self.symbols[self.reels[row][col]]
                color = (200, 0, 0) if symbol == '7' else (0, 0, 0)
                text = self.font.render(symbol, True, color)
                text_rect = text.get_rect(center=(self.x + 90 + col*100, 
                                                self.y + 140 + row*100))
                self.screen.blit(text, text_rect)
        
        # 당첨 구조
        win_infos = [
            ("WIN TABLE", (255, 215, 0)),
            ("777 THREE LINES: x5000", (255, 255, 255)),
            ("777 TWO LINES: x200", (255, 255, 255)),
            ("777 ONE LINE: x10", (255, 255, 255)),
            ("SAME LINE: x3", (200, 200, 200)),
            ("SAME DIAG: x5", (200, 200, 200))
        ]
        
        for i, (info, color) in enumerate(win_infos):
            text = self.small_font.render(info, True, color)
            text_rect = text.get_rect(left=self.x + 30, 
                                    top=self.y + 400 + i*30)
            self.screen.blit(text, text_rect)
        
        # 베팅 컨트롤
        pygame.draw.rect(self.screen, (40, 40, 40), 
                        (self.x + 50, self.y + 520, 300, 40))
        bet_text = self.title_font.render(f"BET: {self.bet_amount}", True, (0, 255, 0))
        bet_rect = bet_text.get_rect(center=(self.x + 200, self.y + 540))
        self.screen.blit(bet_text, bet_rect)
        
        # 베팅 버튼
        for i, (text, x) in enumerate([("-", self.x + 20), ("+", self.x + 330)]):
            pygame.draw.rect(self.screen, (200, 200, 200), (x, self.y + 520, 40, 40))
            btn_text = self.font.render(text, True, (0, 0, 0))
            btn_rect = btn_text.get_rect(center=(x + 20, self.y + 540))
            self.screen.blit(btn_text, btn_rect)
        
        # 자동 스핀 버튼
        auto_color = (50, 200, 50) if self.auto_spin else (200, 50, 50)
        pygame.draw.rect(self.screen, auto_color, 
                        (self.x, self.y + panel_height, panel_width, 40))
        auto_text = self.small_font.render(f"AUTO SPIN: {'ON' if self.auto_spin else 'OFF'}", 
                                         True, (255, 255, 255))
        auto_rect = auto_text.get_rect(center=(self.x + panel_width//2, 
                                             self.y + panel_height + 20))
        self.screen.blit(auto_text, auto_rect) 
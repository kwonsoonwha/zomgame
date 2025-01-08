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
        self.auto_spin = False  # 자동 스핀 상태
        self.spin_time = 0
        self.win_amount = 0
        self.result_timer = 0
        
        # 시스템 폰트 직접 사용
        self.font = pygame.font.SysFont('arial', 36)
        self.small_font = pygame.font.SysFont('arial', 24)
        self.title_font = pygame.font.SysFont('arial', 28)
        
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
        # 메� 패널 - 그라데이션 효과
        for i in range(30):
            color = (140 + i, 140 + i, 140 + i)
            pygame.draw.rect(self.screen, color, (460, 30 + i, 300, 460 - i))
        
        # 제목 패널 - 금속 느낌
        pygame.draw.rect(self.screen, (100, 100, 120), (465, 35, 290, 45))
        pygame.draw.rect(self.screen, (180, 180, 200), (465, 40, 290, 35))
        
        # 제목
        title = self.title_font.render("SLOT MACHINE", True, (50, 50, 50))
        title_shadow = self.title_font.render("SLOT MACHINE", True, (255, 255, 255))
        title_rect = title.get_rect(center=(610, 58))
        shadow_rect = title_shadow.get_rect(center=(612, 60))
        self.screen.blit(title_shadow, shadow_rect)  # 그림자 효과
        self.screen.blit(title, title_rect)
        
        # 릴 배경 - 입체감 있는 프레임
        pygame.draw.rect(self.screen, (60, 60, 60), (480, 95, 260, 240))
        pygame.draw.rect(self.screen, (200, 200, 200), (483, 98, 254, 234))
        pygame.draw.rect(self.screen, (100, 100, 100), (485, 100, 250, 230))
        
        # 각 릴의 심볼
        for row in range(3):
            for col in range(3):
                # 심볼 배경 - 그라데이션과 테두리
                for i in range(3):
                    color = (250 - i*5, 250 - i*5, 250 - i*5)
                    pygame.draw.rect(self.screen, color, 
                                   (490 + col*85 + i, 105 + row*75 + i, 70 - i*2, 65 - i*2))
                
                # 심볼 표시
                symbol = self.symbols[self.reels[row][col]]
                if symbol == '7':  # 7은 빨간색으로
                    color = (200, 50, 50)
                else:
                    color = (50, 50, 50)
                text = self.font.render(symbol, True, color)
                text_rect = text.get_rect(center=(525 + col*85, 138 + row*75))
                
                # 빛나는 효과 (회전 중이거나 당첨 시)
                if self.spinning or (not self.spinning and self.win_amount > 0):
                    glow = pygame.Surface((74, 69), pygame.SRCALPHA)
                    pygame.draw.rect(glow, (255, 255, 200, 50), glow.get_rect())
                    self.screen.blit(glow, (488 + col*85, 103 + row*75))
                
                self.screen.blit(text, text_rect)
        
        # 당첨 구조 - 고급스러운 패널
        win_panel = pygame.Surface((260, 120))
        win_panel.fill((80, 80, 100))
        win_panel.set_alpha(200)
        self.screen.blit(win_panel, (480, 340))
        
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
            text_rect = text.get_rect(left=490, top=350 + i*22)
            self.screen.blit(text, text_rect)
        
        # 베팅 컨트롤 패널 - 입체적인 디자인
        pygame.draw.rect(self.screen, (100, 100, 120), (480, 420, 260, 55))
        pygame.draw.rect(self.screen, (160, 160, 180), (483, 423, 254, 49))
        
        # 베팅 버튼 - 3D 효과
        for i, (text, x) in enumerate([("-", 490), ("+", 700)]):
            # 버튼 그림자
            pygame.draw.rect(self.screen, (80, 80, 80), (x, 427, 35, 35))
            # 버튼 본체
            pygame.draw.rect(self.screen, (180, 180, 180), (x, 425, 35, 35))
            # 버튼 하이라이트
            pygame.draw.rect(self.screen, (220, 220, 220), (x+2, 425, 31, 2))
            
            btn_text = self.font.render(text, True, (50, 50, 50))
            btn_rect = btn_text.get_rect(center=(x + 17, 442))
            self.screen.blit(btn_text, btn_rect)
        
        # 베팅 금액 - 디지털 디스플레이 스타일
        bet_bg = pygame.Surface((120, 35))
        bet_bg.fill((40, 40, 40))
        self.screen.blit(bet_bg, (550, 425))
        
        bet_text = self.title_font.render(f"BET: {self.bet_amount}", True, (0, 255, 0))
        bet_rect = bet_text.get_rect(center=(610, 442))
        self.screen.blit(bet_text, bet_rect)
        
        # 당첨 효과
        if not self.spinning and self.win_amount > 0:
            # 반짝이는 효과
            alpha = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 200
            win_surface = pygame.Surface((200, 40))
            win_surface.fill((50, 200, 50))
            win_surface.set_alpha(alpha)
            win_rect = win_surface.get_rect(center=(610, 300))
            self.screen.blit(win_surface, win_rect)
            
            # 당첨 텍스트
            win_text = self.title_font.render(f"WIN! +{self.win_amount}", True, (255, 255, 100))
            win_shadow = self.title_font.render(f"WIN! +{self.win_amount}", True, (50, 100, 50))
            shadow_rect = win_shadow.get_rect(center=(612, 302))
            text_rect = win_text.get_rect(center=(610, 300))
            self.screen.blit(win_shadow, shadow_rect)
            self.screen.blit(win_text, text_rect) 
        
        # 자동 스핀 버튼 추가
        auto_color = (50, 200, 50) if self.auto_spin else (200, 50, 50)
        pygame.draw.rect(self.screen, auto_color, (480, 480, 260, 35))
        auto_text = self.small_font.render("AUTO SPIN: " + ("ON" if self.auto_spin else "OFF"), True, (255, 255, 255))
        auto_rect = auto_text.get_rect(center=(610, 497))
        self.screen.blit(auto_text, auto_rect) 
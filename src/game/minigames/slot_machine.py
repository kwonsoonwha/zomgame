import pygame
import random
import math

class SlotMachine:
    def __init__(self, screen):
        print("슬롯머신 초기화")
        self.screen = screen
        screen_width = screen.get_width()
        self.x = (screen_width // 2) - 400
        self.y = 50
        
        self.reels = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        self.spinning = [False, False, False]
        self.spin_speed = [0, 0, 0]
        self.spin_timer = [0, 0, 0]
        self.spin_duration = 2000
        self.game_state = "READY"
        
        self.bet_amount = 100
        self.min_bet = 100
        self.win_amount = 0
        
        self.auto_spin = False
        self.auto_spin_timer = 0
        self.auto_spin_delay = 3000
        self.can_toggle_auto = True
        
        self.winning_lines = []
        self.win_message = ""
        self.win_message_timer = 0
        self.win_message_duration = 5000
        self.showing_win = False
        print("초기화 완료:", self.__dict__)
        
    def handle_click(self, pos, current_gold):
        x, y = pos
        
        # 게임이 진행 중일 때는 클릭 무시
        if self.game_state != "READY":
            return False
            
        # AUTO SPIN 버튼 영역
        if (self.x <= x <= self.x + 400 and 
            self.y + 300 <= y <= self.y + 340):
            print(f"Auto spin 버튼 클릭 - 현재 상태: {self.auto_spin}, 게임 상태: {self.game_state}")
            
            # READY 상태일 때만 토글 가능
            if self.game_state == "READY":
                self.auto_spin = not self.auto_spin
                print(f"Auto spin 상태 변경: {self.auto_spin}")
                
                if self.auto_spin:
                    self.auto_spin_timer = pygame.time.get_ticks()
                else:
                    self.auto_spin_timer = 0
            return False
            
        # 베팅 금액 조절 버튼
        if self.y + 240 <= y <= self.y + 280:
            if self.x + 20 <= x <= self.x + 60:  # - 버튼
                self.bet_amount = max(self.min_bet, self.bet_amount - 50)
                return False
            elif self.x + 330 <= x <= self.x + 370:  # + 버튼
                self.bet_amount += 50
                return False
        
        return True
        
    def start_spin(self):
        print(f"스핀 시작 - 게임 상태: {self.game_state}")
        if self.game_state != "READY":
            print("스핀 불가: 게임이 준비 상태가 아님")
            return
            
        current_time = pygame.time.get_ticks()
        self.game_state = "SPINNING"
        for i in range(3):
            self.spinning[i] = True
            self.spin_timer[i] = current_time + i * 500  # 릴마다 시차를 둠
            self.spin_speed[i] = 30
        print(f"스핀 시작 완료 - 타이머: {self.spin_timer}")
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # READY 상태가 아닐 때 자동 스핀 강제 해제
        if self.game_state != "READY" and self.auto_spin:
            print("게임 진행 중 자동 스핀 상태 확인")
            if not any(self.spinning):  # 모든 릴이 멈췄을 때
                print("모든 릴 정지, 자동 스핀 재활성화 가능")
                self.auto_spin_timer = current_time
        
        if self.game_state == "READY":
            if self.auto_spin:
                if current_time - self.auto_spin_timer >= self.auto_spin_delay:
                    print("자동 스핀 작동")
                    self.auto_spin_timer = current_time
                    return True
            return False
        
        # 스핀 업데이트
        spinning = False
        for i in range(3):
            if self.spinning[i]:
                spinning = True
                elapsed = current_time - self.spin_timer[i]
                
                if elapsed >= self.spin_duration:
                    print(f"릴 {i} 정지")
                    self.spinning[i] = False
                    self.spin_timer[i] = 0
                    self.spin_speed[i] = 0
                    # 결과값 정수로 반올림
                    for j in range(3):
                        self.reels[i][j] = round(self.reels[i][j]) % 5
                else:
                    # 회전 속도 조절
                    if elapsed < self.spin_duration * 0.7:
                        self.spin_speed[i] = 30
                    else:
                        self.spin_speed[i] = max(0, 30 * (1 - (elapsed - self.spin_duration * 0.7) / (self.spin_duration * 0.3)))
                    
                    # 릴 회전
                    for j in range(3):
                        self.reels[i][j] = (self.reels[i][j] + self.spin_speed[i] / 60) % 5
                        
        if not spinning and self.game_state == "SPINNING":
            print("모든 릴 정지, 결과 확인")
            print("최종 릴 상태:", self.reels)
            self.game_state = "READY"
            self.check_win()
        
        return False
        
    def check_win(self):
        print("\n당첨 확인 시작")
        print("현재 릴 상태:", self.reels)
        self.win_amount = 0
        seven_lines = 0
        self.winning_lines = []
        win_details = []
        
        # 7의 총 개수 카운트
        total_sevens = sum(1 for reel in self.reels for symbol in reel if symbol == 0)
        print(f"전체 7의 개수: {total_sevens}")
        
        if total_sevens >= 4:
            bonus = self.bet_amount * 10
            self.win_amount += bonus
            win_details.append(f"7 {total_sevens}개: +{bonus}")
            print(f"7 보너스 당첨: {bonus}")
        
        # 가로줄 체크
        for i in range(3):
            if self.reels[0][i] == self.reels[1][i] == self.reels[2][i]:
                if self.reels[0][i] == 0:  # 777
                    seven_lines += 1
                    self.winning_lines.append(("H", i))  # H는 가로(Horizontal)
                else:
                    self.winning_lines.append(("H", i))
                    symbols = ["7", "A", "K", "Q", "J"]
                    multipliers = [10, 5, 4, 3, 2]
                    win = self.bet_amount * multipliers[self.reels[0][i]]
                    self.win_amount += win
                    win_details.append(f"{symbols[self.reels[0][i]]} 3개 (가로): +{win}")
        
        # 세로줄 체크 추가
        for i in range(3):  # 각 릴
            if self.reels[i][0] == self.reels[i][1] == self.reels[i][2]:
                if self.reels[i][0] == 0:  # 777
                    seven_lines += 1
                    self.winning_lines.append(("V", i))  # V는 세로(Vertical)
                else:
                    self.winning_lines.append(("V", i))
                    symbols = ["7", "A", "K", "Q", "J"]
                    multipliers = [10, 5, 4, 3, 2]
                    win = self.bet_amount * multipliers[self.reels[i][0]]
                    self.win_amount += win
                    win_details.append(f"{symbols[self.reels[i][0]]} 3개 (세로): +{win}")
        
        # 777 라인 수에 따른 보상
        if seven_lines > 0:
            if seven_lines == 1:
                win = self.bet_amount * 10
                self.win_amount += win
                win_details.append(f"777 1줄: +{win}")
            elif seven_lines == 2:
                win = self.bet_amount * 500
                self.win_amount += win
                win_details.append(f"777 2줄: +{win}")
            elif seven_lines >= 3:  # 3줄 이상으로 수정
                win = self.bet_amount * 10000
                self.win_amount += win
                win_details.append(f"777 {seven_lines}줄: +{win}")
        
        # 당첨 메시지 설정
        if self.win_amount > 0:
            self.win_message = f"축하합니다!\n총 당첨금: {self.win_amount}\n" + "\n".join(win_details)
            self.win_message_timer = pygame.time.get_ticks()
            self.showing_win = True
        
        print(f"최종 당첨금: {self.win_amount}")
        print(f"당첨 라인: {self.winning_lines}")
        print(f"당첨 내역: {win_details}\n")
        
    def draw(self):
        # 배경
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (self.x, self.y, 400, 500))
        
        # 릴 그리기
        symbols = ["7", "A", "K", "Q", "J"]
        for i in range(3):  # 각 릴
            for j in range(3):  # 각 심볼
                symbol_index = int(self.reels[i][j]) % 5
                symbol = symbols[symbol_index]
                
                # 심볼 색상 설정
                if symbol == "7":
                    color = (255, 215, 0)  # 골드
                elif symbol == "A":
                    color = (255, 0, 0)    # 빨강
                elif symbol == "K":
                    color = (0, 255, 0)    # 초록
                elif symbol == "Q":
                    color = (0, 0, 255)    # 파랑
                else:
                    color = (255, 255, 255) # 흰색
                
                # 심볼 그리기
                font = pygame.font.SysFont('arial', 48)
                text = font.render(symbol, True, color)
                text_rect = text.get_rect(center=(self.x + 100 + i * 100, 
                                                self.y + 100 + j * 100))
                self.screen.blit(text, text_rect)
                
                # 심볼 테두리
                pygame.draw.rect(self.screen, (50, 50, 50),
                               (self.x + 50 + i * 100,
                                self.y + 50 + j * 100,
                                100, 100), 2)
        
        # 당첨 라인 표시
        if self.winning_lines:
            for line_type, index in self.winning_lines:
                if line_type == "H":  # 가로 라인
                    y = self.y + 100 + index * 100
                    pygame.draw.line(self.screen, (255, 255, 0),
                                   (self.x + 50, y),
                                   (self.x + 350, y), 3)
                elif line_type == "V":  # 세로 라인
                    x = self.x + 100 + index * 100
                    pygame.draw.line(self.screen, (255, 255, 0),
                                   (x, self.y + 50),
                                   (x, self.y + 350), 3)
        
        # 베팅 금액 표시
        font = pygame.font.SysFont('malgungothic', 36)
        bet_text = font.render(f"베팅: {self.bet_amount}", True, (255, 255, 255))
        self.screen.blit(bet_text, (self.x + 150, self.y + 250))
        
        # 베팅 조절 버튼
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (self.x + 20, self.y + 240, 40, 40))  # - 버튼
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (self.x + 330, self.y + 240, 40, 40))  # + 버튼
        
        button_font = pygame.font.SysFont('arial', 36)
        minus = button_font.render("-", True, (0, 0, 0))
        plus = button_font.render("+", True, (0, 0, 0))
        self.screen.blit(minus, (self.x + 32, self.y + 245))
        self.screen.blit(plus, (self.x + 342, self.y + 245))
        
        # AUTO SPIN 버튼 상태 표시
        auto_color = (50, 200, 50) if self.auto_spin else (200, 50, 50)
        button_color = auto_color if self.game_state == "READY" else (150, 150, 150)
        
        pygame.draw.rect(self.screen, button_color, 
                        (self.x, self.y + 300, 400, 40))
        
        font = pygame.font.SysFont('malgungothic', 36)
        auto_text = font.render(f"AUTO SPIN: {'ON' if self.auto_spin else 'OFF'}", 
                              True, (255, 255, 255))
        auto_rect = auto_text.get_rect(center=(self.x + 200, self.y + 320))
        self.screen.blit(auto_text, auto_rect)
        
        # 게임 상태가 READY가 아닐 때 버튼 비활성화 표시
        if self.game_state != "READY":
            s = pygame.Surface((400, 40))
            s.set_alpha(128)
            s.fill((100, 100, 100))
            self.screen.blit(s, (self.x, self.y + 300))
        
        # 당첨 메시지 표시
        current_time = pygame.time.get_ticks()
        if self.showing_win and current_time - self.win_message_timer < self.win_message_duration:
            message_font = pygame.font.SysFont('malgungothic', 24)
            y_offset = 0
            for line in self.win_message.split('\n'):
                text = message_font.render(line, True, (255, 255, 0))
                text_rect = text.get_rect(center=(self.x + 200, self.y + 400 + y_offset))
                padding = 5
                bg_rect = pygame.Rect(text_rect.x - padding, 
                                    text_rect.y - padding,
                                    text_rect.width + padding * 2, 
                                    text_rect.height + padding * 2)
                pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
                self.screen.blit(text, text_rect)
                y_offset += 30
        elif self.showing_win and current_time - self.win_message_timer >= self.win_message_duration:
            self.showing_win = False  # 표시 시간 종료
            print("당첨금 표시 종료")  # 디버깅용
        
    def show_error(self, message):
        self.error_message = message
        self.error_timer = pygame.time.get_ticks() 
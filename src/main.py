import pygame
import sys
import random
from game.unit import Unit
from game.castle import Castle
from game.minigames.slot_machine import SlotMachine
from game.minigames.rps_game import RPSGame

# 화면 설정
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CASTLE_WIDTH = 200
CASTLE_HEIGHT = 400

class Button:
    def __init__(self, x, y, width, height, text, color, unit_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.unit_type = unit_type
        
        try:
            self.font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 24)
            self.small_font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 16)
        except:
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 16)
        
        self.hover = False
        
        self.unit_info = {
            'warrior': {'cost': 100, 'hp': 100, 'atk': 10, 'speed': '빠름'},
            'archer': {'cost': 150, 'hp': 70, 'atk': 15, 'speed': '보통'},
            'knight': {'cost': 200, 'hp': 150, 'atk': 20, 'speed': '느림'}
        }
        
    def draw(self, screen, gold):
        # 버튼 배경
        if self.hover:
            pygame.draw.rect(screen, (min(self.color[0] + 30, 255), 
                                    min(self.color[1] + 30, 255), 
                                    min(self.color[2] + 30, 255)), self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            
        # 테두리
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        
        # 유닛 이름
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(midtop=(self.rect.centerx, self.rect.y + 5))
        screen.blit(text_surface, text_rect)
        
        # 비용
        cost_text = self.font.render(f"비용: {self.unit_info[self.unit_type]['cost']}", True, 
                                   (0, 0, 0) if gold >= self.unit_info[self.unit_type]['cost'] else (255, 0, 0))
        screen.blit(cost_text, (self.rect.x + 10, self.rect.y + 30))
        
        # 스탯 정보
        stats = [
            f"체력: {self.unit_info[self.unit_type]['hp']}",
            f"공격력: {self.unit_info[self.unit_type]['atk']}",
            f"속도: {self.unit_info[self.unit_type]['speed']}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.small_font.render(stat, True, (0, 0, 0))
            screen.blit(stat_text, (self.rect.x + 10, self.rect.y + 55 + (i * 20)))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Castle Battle")
        
        self.left_castle = Castle(self.screen, "left", "player")
        self.right_castle = Castle(self.screen, "right", "ai")
        self.slot_machine = SlotMachine(self.screen)
        self.rps_game = RPSGame(self.screen)
        
        # 골드 자동 증가를 위한 타이머 추가
        self.last_gold_update = pygame.time.get_ticks()
        self.gold_update_delay = 100  # 0.1초마다 업데이트 (1초에 10골드)

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            current_time = pygame.time.get_ticks()
            
            # 골드 자동 증가 처리
            if current_time - self.last_gold_update >= self.gold_update_delay:
                self.left_castle.gold += 1  # 왼쪽 플레이어 (사람)
                self.right_castle.gold += 1  # 오른쪽 플레이어 (AI)
                self.last_gold_update = current_time
            
            # 슬롯머신 업데이트
            if self.slot_machine.auto_spin and not self.slot_machine.spinning:
                if self.left_castle.gold >= self.slot_machine.bet_amount:
                    gold_change = self.slot_machine.spin()
                    self.left_castle.gold += gold_change
            
            # 슬롯머신 진행 중인 경우 업데이트
            if self.slot_machine.spinning:
                win_amount = self.slot_machine.update()
                if win_amount > 0:
                    self.left_castle.gold += win_amount
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # 슬롯머신 베팅 조절
                    if 490 <= mouse_pos[0] <= 525 and 425 <= mouse_pos[1] <= 460:  # - 버튼
                        self.slot_machine.change_bet(False)
                    elif 700 <= mouse_pos[0] <= 735 and 425 <= mouse_pos[1] <= 460:  # + 버튼
                        self.slot_machine.change_bet(True)
                    
                    # 자동 스핀 토글 버튼
                    elif 480 <= mouse_pos[0] <= 740 and 480 <= mouse_pos[1] <= 515:
                        self.slot_machine.auto_spin = not self.slot_machine.auto_spin
                        if self.slot_machine.auto_spin and not self.slot_machine.spinning:
                            if self.left_castle.gold >= self.slot_machine.bet_amount:
                                gold_change = self.slot_machine.spin()
                                self.left_castle.gold += gold_change
                    
                    # 슬롯머신 수동 스핀
                    elif (480 <= mouse_pos[0] <= 740 and 95 <= mouse_pos[1] <= 335 and 
                          not self.slot_machine.spinning):
                        if self.left_castle.gold >= self.slot_machine.bet_amount:
                            gold_change = self.slot_machine.spin()
                            self.left_castle.gold += gold_change
            
            # 화면 업데이트
            self.screen.fill((50, 168, 82))  # 초록색 배경
            self.left_castle.draw()
            self.right_castle.draw()
            self.slot_machine.draw()
            self.rps_game.draw()
            pygame.display.flip()
            
            clock.tick(60)  # FPS 제한

if __name__ == "__main__":
    game = Game()
    game.run() 
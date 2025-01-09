import pygame
from game.castle import Castle
from game.minigames.slot_machine import SlotMachine
from game.minigames.rps_game import RPSGame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Castle Battle")
        
        # 클럭 초기화 추가
        self.clock = pygame.time.Clock()
        
        # 게임 객체 초기화
        self.left_castle = Castle(self.screen, "left", "player")
        self.right_castle = Castle(self.screen, "right", "ai")
        self.slot_machine = SlotMachine(self.screen)
        self.rps_game = RPSGame(self.screen)
        
        # 초기 골드 설정
        self.left_castle.gold = 1000
        self.right_castle.gold = 1000
        
        # 폰트 초기화
        pygame.font.init()
        
        # 크레딧 정보
        self.credit_font = pygame.font.SysFont('malgungothic', 20)
        self.credit_text = "만든이: 전석우"
        self.ad_text = "무료 충전: http://www.naver.com"
        
    def draw(self):
        self.screen.fill((50, 50, 50))  # 배경
        
        # 게임 요소들 그리기
        self.left_castle.draw()
        self.right_castle.draw()
        self.slot_machine.draw()
        self.rps_game.draw()
        
        # 크레딧 정보 그리기 (우측 상단)
        credit = self.credit_font.render(self.credit_text, True, (255, 255, 255))
        credit_rect = credit.get_rect(topright=(self.screen.get_width() - 20, 20))
        
        # 배경 추가
        padding = 5
        bg_rect = pygame.Rect(credit_rect.x - padding,
                            credit_rect.y - padding,
                            credit_rect.width + padding * 2,
                            credit_rect.height + padding * 2)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
        self.screen.blit(credit, credit_rect)
        
        # 광고 정보 그리기 (우측 상단, 크레딧 아래)
        ad = self.credit_font.render(self.ad_text, True, (255, 255, 0))  # 노란색으로 표시
        ad_rect = ad.get_rect(topright=(self.screen.get_width() - 20, 50))
        
        # 배경 추가
        bg_rect = pygame.Rect(ad_rect.x - padding,
                            ad_rect.y - padding,
                            ad_rect.width + padding * 2,
                            ad_rect.height + padding * 2)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
        self.screen.blit(ad, ad_rect)
        
        pygame.display.flip()
        
    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # 왼쪽 성 유닛 생산
                    self.left_castle.handle_click(mouse_pos)
                    
                    # 슬롯머신 클릭 처리
                    if self.slot_machine.handle_click(mouse_pos, self.left_castle.gold):
                        if self.left_castle.gold >= self.slot_machine.bet_amount:
                            self.left_castle.gold -= self.slot_machine.bet_amount
                            self.slot_machine.start_spin()
                    
                    # 가위바위보 클릭 처리
                    if self.rps_game.handle_click(mouse_pos):
                        if self.left_castle.gold >= self.rps_game.bet_amount:
                            self.left_castle.gold -= self.rps_game.bet_amount
            
            # AI 처리 (오른쪽 성)
            if current_time % 3000 < 50:  # 3초마다
                if self.right_castle.gold >= 150:  # 중간 가격 유닛
                    self.right_castle.produce_unit(random.choice(["전사", "궁수", "기사"]))
            
            # 성 업데이트 (전투 포함)
            self.left_castle.update(self.right_castle)
            self.right_castle.update(self.left_castle)
            
            # 게임 오버 체크
            if self.left_castle.health <= 0:
                print("오른쪽 성 승리!")
                pygame.quit()
                return
            elif self.right_castle.health <= 0:
                print("왼쪽 성 승리!")
                pygame.quit()
                return
            
            # 슬롯머신 업데이트
            if self.slot_machine.update():
                if self.left_castle.gold >= self.slot_machine.bet_amount:
                    self.left_castle.gold -= self.slot_machine.bet_amount
                    self.slot_machine.start_spin()
            
            # 슬롯머신 당첨금 처리
            if (self.slot_machine.game_state == "READY" and 
                self.slot_machine.win_amount > 0):
                self.left_castle.gold += self.slot_machine.win_amount
                self.slot_machine.win_amount = 0
            
            # 가위바위보 업데이트 및 결과 처리
            result = self.rps_game.update()
            if result != 0:
                self.left_castle.gold += result
            
            # 화면 그리기
            self.draw()
            
            # FPS 설정
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run() 
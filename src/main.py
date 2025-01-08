import pygame
from game.castle import Castle
from game.minigames.slot_machine import SlotMachine
from game.minigames.rps_game import RPSGame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Castle Battle")
        
        # 게임 객체 초기화
        self.left_castle = Castle(self.screen, "left", "player")
        self.right_castle = Castle(self.screen, "right", "ai")
        self.slot_machine = SlotMachine(self.screen)
        self.rps_game = RPSGame(self.screen)
        
        # 초기 골드 설정
        self.left_castle.gold = 1000
        self.right_castle.gold = 1000
        
    def draw(self):
        # 배경
        self.screen.fill((34, 139, 34))  # 초록색 배경
        
        # 성 그리기
        self.left_castle.draw()
        self.right_castle.draw()
        
        # 미니게임 그리기
        self.slot_machine.draw()
        self.rps_game.draw()
        
        # 화면 업데이트
        pygame.display.flip()
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # 슬롯머신 클릭 처리
                    if self.slot_machine.handle_click(mouse_pos, self.left_castle.gold):
                        self.left_castle.gold -= self.slot_machine.bet_amount
                        self.slot_machine.start_spin()
            
            # 슬롯머신 업데이트
            self.slot_machine.update()
            
            # 당첨금 지급 (PAYING 상태가 끝날 때)
            if (self.slot_machine.game_state == "READY" and 
                self.slot_machine.win_amount > 0):
                self.left_castle.gold += self.slot_machine.win_amount
                self.slot_machine.win_amount = 0
            
            # 화면 그리기
            self.draw()
            
            # FPS 설정
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run() 
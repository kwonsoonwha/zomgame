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
        
        # 유닛 리스트 추가
        self.units = []
        
        # 골드 자동 증가를 위한 타이머
        self.last_gold_update = pygame.time.get_ticks()
        self.gold_update_delay = 100
        
        # AI 관련 �수 추가
        self.ai_strategy = {
            "aggressive": {
                "전사": 0.6,  # 전사 생산 확률
                "궁수": 0.3,  # 궁수 생산 확률
                "기사": 0.1   # 기사 생산 확률
            },
            "defensive": {
                "전사": 0.3,
                "궁수": 0.5,
                "기사": 0.2
            }
        }
        self.ai_mode = "aggressive"  # 기본 전략
        self.ai_action_delay = 1500  # 1.5초마다 결정
        self.last_ai_action = pygame.time.get_ticks()
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            current_time = pygame.time.get_ticks()
            
            # 골드 자동 증가
            if current_time - self.last_gold_update >= self.gold_update_delay:
                self.left_castle.gold += 1
                self.right_castle.gold += 1
                self.last_gold_update = current_time
            
            # AI 행동 업데이트
            if current_time - self.last_ai_action >= self.ai_action_delay:
                self.ai_action()
                self.last_ai_action = current_time
            
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # 유닛 생산 버튼 클릭 처리
                    unit_type = self.left_castle.check_unit_click(mouse_pos)
                    if unit_type:
                        new_unit = self.left_castle.create_unit(unit_type)
                        if new_unit:
                            self.units.append(new_unit)
                    
                    # 기존의 미니게임 클릭 처리...
            
            # 유닛 업데이트
            self.update_units()
            
            # 화면 그리기
            self.screen.fill((50, 168, 82))
            self.left_castle.draw()
            self.right_castle.draw()
            
            # 유닛 그리기
            for unit in self.units:
                unit.draw()
            
            self.slot_machine.draw()
            self.rps_game.draw()
            pygame.display.flip()
            
            clock.tick(60)
            
    def update_units(self):
        # 죽은 유닛 제거
        self.units = [unit for unit in self.units if not unit.is_dead()]
        
        for unit in self.units:
            unit.move()
            
            # 유닛 충돌 체크
            for other in self.units:
                if unit != other and self.check_collision(unit, other):
                    if unit.position != other.position:  # 적대적 유닛끼리만 전투
                        unit.take_damage(other.attack)
                        other.take_damage(unit.attack)
            
            # 성 공격 체크
            if unit.position == "left" and unit.x >= 1620:  # 오른쪽 성 공격
                self.right_castle.take_damage(unit.attack)
                unit.health = 0  # 공격 후 소멸
            elif unit.position == "right" and unit.x <= 300:  # 왼쪽 성 공격
                self.left_castle.take_damage(unit.attack)
                unit.health = 0  # 공격 후 소멸
                
    def check_collision(self, unit1, unit2):
        # 간단한 원형 충돌 체크
        distance = ((unit1.x - unit2.x) ** 2 + (unit1.y - unit2.y) ** 2) ** 0.5
        return distance < (unit1.size + unit2.size)
        
    def ai_action(self):
        # AI가 현재 상황을 분석
        player_units = [u for u in self.units if u.position == "left"]
        ai_units = [u for u in self.units if u.position == "right"]
        
        # 전략 선택
        if self.right_castle.health < 50:  # 체력이 낮으면 방어적
            self.ai_mode = "defensive"
        elif len(player_units) > len(ai_units) + 2:  # 상대 유닛이 많으면 방어적
            self.ai_mode = "defensive"
        else:
            self.ai_mode = "aggressive"
        
        # 유닛 생산 결정
        if self.right_castle.gold >= 100:  # 최소 비용
            # 현재 전략에 따른 확률 분포 사용
            weights = list(self.ai_strategy[self.ai_mode].values())
            unit_types = list(self.ai_strategy[self.ai_mode].keys())
            
            # 상황에 따른 추가 조정
            if self.right_castle.gold >= 200:  # 골드가 충분하면
                choice = random.choices(unit_types, weights=weights)[0]
                new_unit = self.right_castle.create_unit(choice)
                if new_unit:
                    self.units.append(new_unit)
            elif self.right_castle.gold >= 150:  # 중간 정도의 골드
                # 전사나 궁수만 생산
                if random.random() < 0.7:  # 70% 확률로 생산
                    choice = random.choice(["전사", "궁수"])
                    new_unit = self.right_castle.create_unit(choice)
                    if new_unit:
                        self.units.append(new_unit)
            else:  # 골드가 적을 때
                # 전사만 생산
                if random.random() < 0.5:  # 50% 확률로 생산
                    new_unit = self.right_castle.create_unit("전사")
                    if new_unit:
                        self.units.append(new_unit)

if __name__ == "__main__":
    game = Game()
    game.run() 
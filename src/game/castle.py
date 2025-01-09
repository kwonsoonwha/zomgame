import pygame
from .unit import Unit

class Castle:
    def __init__(self, screen, position, owner):
        self.screen = screen
        self.position = position
        self.owner = owner
        self.gold = 1000
        self.health = 1000000
        self.max_health = 1000000
        self.units = []
        self.projectiles = []
        
        # 성 공격 관련 추가
        self.castle_damage = 2  # 성의 공격력
        self.castle_attack_range = 300  # 성의 공격 범위
        self.castle_attack_cooldown = 0  # 공격 쿨다운
        self.castle_attack_delay = 1000  # 1초
        
        # 유닛 스탯
        self.unit_stats = {
            "전사": {"health": 100, "damage": 50, "range": 20, "cost": 100, "speed": 0.4},
            "궁수": {"health": 80, "damage": 40, "range": 150, "cost": 150, "speed": 0.4},
            "기사": {"health": 150, "damage": 75, "range": 30, "cost": 200, "speed": 0.4}
        }
        
        self.gold_timer = 0
        self.gold_increment = 10
        self.gold_delay = 1000
        
        self.production_cooldown = 0
        self.cooldown_time = 1000
        
    def handle_click(self, pos):
        x, y = pos
        
        # 유닛 생산 버튼 영역
        button_y = 680  # 버튼 Y 위치
        if button_y <= y <= button_y + 40:
            # 왼쪽 성일 경우
            if self.position == "left":
                if 50 <= x <= 150:  # 전사 버튼
                    return self.produce_unit("전사")
                elif 160 <= x <= 260:  # 궁수 버튼
                    return self.produce_unit("궁수")
                elif 270 <= x <= 370:  # 기사 버튼
                    return self.produce_unit("기사")
            # 오른쪽 성일 경우
            else:
                if self.screen.get_width() - 370 <= x <= self.screen.get_width() - 270:
                    return self.produce_unit("전사")
                elif self.screen.get_width() - 260 <= x <= self.screen.get_width() - 160:
                    return self.produce_unit("궁수")
                elif self.screen.get_width() - 150 <= x <= self.screen.get_width() - 50:
                    return self.produce_unit("기사")
        return False
        
    def produce_unit(self, unit_type):
        current_time = pygame.time.get_ticks()
        
        if current_time < self.production_cooldown:
            return False
            
        unit_cost = self.unit_stats[unit_type]["cost"]
        if self.gold >= unit_cost:
            self.gold -= unit_cost
            
            # 유닛 생성 위치
            if self.position == "left":
                spawn_x = 100
            else:
                spawn_x = self.screen.get_width() - 100
                
            # 유닛 생성 (speed 추가)
            new_unit = {
                "type": unit_type,
                "x": spawn_x,
                "y": 600,
                "health": self.unit_stats[unit_type]["health"],
                "max_health": self.unit_stats[unit_type]["health"],
                "damage": self.unit_stats[unit_type]["damage"],
                "range": self.unit_stats[unit_type]["range"],
                "speed": self.unit_stats[unit_type]["speed"],
                "attack_cooldown": 0
            }
            self.units.append(new_unit)
            
            self.production_cooldown = current_time + self.cooldown_time
            return True
            
        return False
        
    def create_projectile(self, start_pos, target_pos, damage):
        self.projectiles.append({
            "start_x": start_pos[0],
            "start_y": start_pos[1],
            "target_x": target_pos[0],
            "target_y": target_pos[1],
            "damage": damage,
            "speed": 10,
            "distance": 0
        })
        
    def update(self, enemy_castle):
        current_time = pygame.time.get_ticks()
        
        # 적 성의 x 좌표 미리 계산
        enemy_castle_x = 150 if enemy_castle.position == "left" else self.screen.get_width() - 150
        
        # 성의 자동 공격
        if current_time >= self.castle_attack_cooldown:
            castle_x = 150 if self.position == "left" else self.screen.get_width() - 150
            castle_y = 600
            
            # 가장 가까운 적 유닛 찾기
            closest_enemy = None
            min_distance = self.castle_attack_range
            
            for enemy_unit in enemy_castle.units:
                distance = abs(enemy_unit["x"] - castle_x)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy_unit
            
            # 적 유닛이 사거리 안에 있으면 공격
            if closest_enemy:
                self.create_projectile(
                    (castle_x, castle_y),
                    (closest_enemy["x"], closest_enemy["y"]),
                    self.castle_damage
                )
                self.castle_attack_cooldown = current_time + self.castle_attack_delay
        
        # 골드 자동 증가
        if current_time - self.gold_timer >= self.gold_delay:
            self.gold += self.gold_increment
            self.gold_timer = current_time
        
        # 유닛 이동 및 전투
        for unit in self.units:
            # 전투 상태가 아닐 때만 이동
            unit_in_combat = False
            
            # 적 유닛과의 전투 체크
            for enemy_unit in enemy_castle.units:
                distance = abs(unit["x"] - enemy_unit["x"])
                if distance <= unit["range"]:
                    unit_in_combat = True
                    if current_time >= unit["attack_cooldown"]:
                        # 투사체 생성
                        self.create_projectile(
                            (unit["x"], unit["y"]),
                            (enemy_unit["x"], enemy_unit["y"]),
                            unit["damage"]
                        )
                        unit["attack_cooldown"] = current_time + 1000
                    break
            
            # 성과의 전투 체크
            castle_x = 150 if enemy_castle.position == "left" else self.screen.get_width() - 150
            distance_to_castle = abs(unit["x"] - castle_x)
            if distance_to_castle <= unit["range"]:
                unit_in_combat = True
                if current_time >= unit["attack_cooldown"]:
                    # 성 공격용 투사체 생성
                    self.create_projectile(
                        (unit["x"], unit["y"]),
                        (castle_x, 600),
                        unit["damage"] * 2
                    )
                    unit["attack_cooldown"] = current_time + 1000
            
            # 전투 중이 아닐 때만 이동
            if not unit_in_combat:
                if self.position == "left":
                    unit["x"] += unit["speed"]
                else:
                    unit["x"] -= unit["speed"]
        
        # 투사체 업데이트
        for projectile in self.projectiles[:]:
            dx = projectile["target_x"] - projectile["start_x"]
            dy = projectile["target_y"] - projectile["start_y"]
            distance = (dx**2 + dy**2)**0.5
            
            if distance == 0:
                self.projectiles.remove(projectile)
                continue
                
            move_ratio = projectile["speed"] / distance
            projectile["distance"] += projectile["speed"]
            current_x = projectile["start_x"] + dx * move_ratio * projectile["distance"]
            current_y = projectile["start_y"] + dy * move_ratio * projectile["distance"]
            
            if projectile["distance"] >= distance:
                for enemy_unit in enemy_castle.units:
                    if abs(enemy_unit["x"] - projectile["target_x"]) < 10:
                        enemy_unit["health"] -= projectile["damage"]
                        break
                else:
                    if abs(enemy_castle_x - projectile["target_x"]) < 100:  # enemy_castle_x 사용
                        enemy_castle.health -= projectile["damage"]
                
                self.projectiles.remove(projectile)
            else:
                projectile["current_x"] = current_x
                projectile["current_y"] = current_y
        
        # 죽은 유닛 제거
        self.units = [unit for unit in self.units 
                     if unit["health"] > 0 and 
                     0 <= unit["x"] <= self.screen.get_width()]
        
    def draw(self):
        # 성 그리기
        castle_color = (100, 100, 100)
        if self.position == "left":
            castle_x = 50
        else:
            castle_x = self.screen.get_width() - 150
            
        # 성 본체
        pygame.draw.rect(self.screen, castle_color, (castle_x, 500, 100, 200))
        
        # 체력바
        health_ratio = self.health / self.max_health
        health_color = (int(255 * (1 - health_ratio)), int(255 * health_ratio), 0)
        pygame.draw.rect(self.screen, health_color, 
                        (castle_x, 480, 100 * health_ratio, 10))
        
        # 체력 수치 표시
        font = pygame.font.SysFont('malgungothic', 20)
        health_text = font.render(f"HP: {int(self.health)}", True, (255, 255, 255))
        self.screen.blit(health_text, (castle_x, 460))
        
        # 골드 표시 (크고 눈에 띄게)
        gold_font = pygame.font.SysFont('malgungothic', 32)
        gold_text = gold_font.render(f"Gold: {self.gold}", True, (255, 215, 0))
        if self.position == "left":
            gold_x = 50
        else:
            gold_x = self.screen.get_width() - 250
        self.screen.blit(gold_text, (gold_x, 420))
        
        # 유닛 생산 버튼
        button_y = 680
        for i, (unit_type, stats) in enumerate(self.unit_stats.items()):
            if self.position == "left":
                button_x = 50 + i * 110
            else:
                button_x = self.screen.get_width() - 370 + i * 110
                
            color = (150, 150, 150)
            if self.gold >= stats["cost"]:
                color = (200, 200, 200)
                
            pygame.draw.rect(self.screen, color, (button_x, button_y, 100, 40))
            
            # 버튼 텍스트 (유닛 정보 추가)
            text = f"{unit_type}\n{stats['cost']}G"
            y_offset = 0
            for line in text.split('\n'):
                text_surface = font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(
                    center=(button_x + 50, button_y + 10 + y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 20
        
        # 유닛 그리기
        for unit in self.units:
            color = {
                "전사": (255, 0, 0),
                "궁수": (0, 255, 0),
                "기사": (0, 0, 255)
            }[unit["type"]]
            
            # 유닛 본체
            pygame.draw.circle(self.screen, color, 
                             (int(unit["x"]), int(unit["y"])), 10)
            
            # 유닛 체력바
            health_ratio = unit["health"] / unit["max_health"]
            health_width = 20 * health_ratio
            pygame.draw.rect(self.screen, (255, 0, 0),
                           (unit["x"] - 10, unit["y"] - 20, health_width, 5)) 
        
        # 투사체 그리기
        for projectile in self.projectiles:
            if hasattr(projectile, "current_x"):
                pygame.draw.circle(self.screen, (255, 255, 0),
                                 (int(projectile["current_x"]), 
                                  int(projectile["current_y"])), 3) 
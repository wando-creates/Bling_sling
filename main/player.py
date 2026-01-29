import pygame
import random
from pygame.math import Vector2

pygame.font.init()

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x,y,5,5)
        self.speed = 25
        self.direction = direction.normalize()
        self.dead = False
    
    def update(self, tiles):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.dead = True
                return
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,0), self.rect)
    
    def is_off_screen(self, screen_size):
        screen_width, screen_height = screen_size
        return (self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height)
    
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y, 40,40)
        self.speed = 2
        self.health = 3
        self.dead = False

        self.state = "patrol"
        self.patrol_target = None
        self.patrol_timer = 0

    def pick_patrol_target(self, tiles):
        for _ in range(20):
            x = self.rect.centerx + random.randint(-300,300)
            y = self.rect.centery + random.randint(-300,300)
            test_rect = pygame.Rect(x - 20, y - 20, 40, 40)
            
            if not any(test_rect.colliderect(t) for t in tiles):
                self.patrol_target = Vector2(x, y)
                return
    
    def patrol(self, tiles):
        if self.patrol_target is None:
            self.pick_patrol_target(tiles)
            return
        pos = Vector2(self.rect.center)
        direction = self.patrol_target - pos

        if direction.length() < 10:
            self.patrol_target = None
            return
        
        direction = direction.normalize() * (self.speed)
        moved = self.move_with_collisions(direction, tiles)
    
        if not moved:
            self.patrol_target = None
            
    def move_with_collisions(self, direction, tiles):
        moved = True

        self.rect.x += direction.x
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.rect.x -= direction.x
                moved = False
                break

        self.rect.y += direction.y
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.rect.y -= direction.y
                moved = False
                break
        
        return moved

    def chase(self, player_pos, tiles):
        pos = Vector2(self.rect.center)
        direction = player_pos - pos
        if direction.length() == 0:
            return
        
        direction = direction.normalize() * self.speed
        self.move_with_collisions(direction, tiles)
    def update(self, player_pos, tiles, can_see_player):

        if self.dead:
            return
        
        if can_see_player:
            self.state = "chase"
        else:
            self.state = "patrol"
            self.patrol(tiles)
            return
        
        pos = Vector2(self.rect.center)

        seek = player_pos  - pos
        if seek.length() > 0:
            seek = seek.normalize()
        
        avoid = Vector2(0,0)
        AVOID_RADIUS = 50

        for tile in tiles:
            if not self.rect.colliderect(tile.inflate(AVOID_RADIUS * 2, AVOID_RADIUS * 2)):
                
                closest_x = max(tile.left, min(pos.x, tile.right))
                closest_y = max(tile.top, min(pos.y, tile.bottom))
                closest = Vector2(closest_x, closest_y)

                diff = pos - closest
                dist = diff.length()

                if 0 < dist < AVOID_RADIUS:
                    strength = (AVOID_RADIUS - dist) / AVOID_RADIUS
                    avoid += diff.normalize() * strength
        
        
        if avoid.length() > 0:
            avoid = avoid.normalize() * 1.5

#------------- COLLISIONS FOR ENEMYS -------------#

        direction = seek  * 1.0 + avoid * 0.8
        if direction.length() == 0:
            return
        
        direction = direction.normalize() * self.speed

        self.rect.x += direction.x

        for tile in tiles:
            if self.rect.colliderect(tile):
                if direction.x > 0:
                    self.rect.right = tile.left
                elif direction.x < 0:
                    self.rect.left = tile.right
        
        self.rect.y += direction.y

        for tile in tiles:
            if self.rect.colliderect(tile):
                if direction.y > 0:
                    self.rect.bottom = tile.top
                elif direction.y < 0:
                    self.rect.top = tile.bottom
                break
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.dead = True
    
    def draw(self, screen):
        if not self.dead:
            pygame.draw.rect(screen, (255,0,0), self.rect)

            health_bar_width = 40
            health_bar_height = 5
            health_width = (self.health / 3) * health_bar_width
            pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.y - 10, health_width, health_bar_height))



class Player:
    def __init__(self, posx, posy):
        self.rect = pygame.Rect(posx, posy, 50, 50)

        self.speed = 5
        self.vel = Vector2(0,0)
        self.bullets = []
    
    def move(self):
        keys = pygame.key.get_pressed()

        self.vel.x = 0
        self.vel.y = 0

        if keys[pygame.K_d]:
            self.vel.x = self.speed
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_w]:
            self.vel.y = -self.speed
        if keys[pygame.K_s]:
            self.vel.y = self.speed

        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

    def shoot(self, mouse_pos):
        player_center = Vector2(self.rect.centerx, self.rect.centery)
        mouse_vec = Vector2(mouse_pos[0], mouse_pos[1])
        direction = mouse_vec - player_center

        if direction.length() > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
            self.bullets.append(bullet)

    def update(self, tiles, enemies, screen_size):
        self.rect.x += self.vel.x 

        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.x > 0:
                    self.rect.right = tile.left
                elif self.vel.x <0:
                    self.rect.left = tile.right
                break

        self.rect.y += self.vel.y 

        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:
                    self.rect.bottom = tile.top
                elif self.vel.y < 0:
                    self.rect.top = tile.bottom
                break


        for bullet in self.bullets[:]:
            bullet.update(tiles)

            for enemy in enemies:
                if not enemy.dead and bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage()
                    bullet.dead = True
                    break
                
            if bullet.is_off_screen(screen_size) or bullet.dead:
                self.bullets.remove(bullet)

    def draw(self, screen, font):
        pygame.draw.rect(screen, (100,100,100), self.rect)

        for bullet in self.bullets:
            bullet.draw(screen)

        velocity_text = font.render(f"Velocity: ({self.vel.x:.2f}, {self.vel.y:.2f})", True, (255,255,255))
        screen.blit(velocity_text, (10,10))

        position_text = font.render(f"Position: ({self.rect.x}, {self.rect.y})", True, (255,255,255))
        screen.blit(position_text, (10,40))





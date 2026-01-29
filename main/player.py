import pygame
from pygame.math import Vector2
pygame.font.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_width(), screen.get_height()
font = pygame.font.SysFont(None, 24)

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x,y,5,5)
        self.speed = 10
        self.direction = direction.normalize()
    
    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,0), self.rect)
    
    def is_off_screen(self):
        return (self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height)


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

    def update(self):
        self.rect.x += self.vel.x 
        self.rect.y += self.vel.y 

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect)

        for bullet in self.bullets:
            bullet.draw(screen)

        velocity_text = font.render(f"Velocity: ({self.vel.x:.2f}, {self.vel.y:.2f})", True, (255,255,255))
        screen.blit(velocity_text, (10,10))

        position_text = font.render(f"Position: ({self.rect.x}, {self.rect.y})", True, (255,255,255))
        screen.blit(position_text, (10,40))

    



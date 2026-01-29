import pygame
import json
from player import Player, Enemy
from pygame.math import Vector2

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_width(), screen.get_height()

font = pygame.font.SysFont(None, 24)

TILE_SIZE = 50

def load_map(filename, tile_size):
    try:
        with open(filename, "r") as f:
            tilemap = json.load(f)
        tiles = []
        for y, row in enumerate(tilemap):
            for x, tile in enumerate(row):
                if tile == 1:
                    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    tiles.append(rect)
        return tiles, tilemap
    except FileNotFoundError:
        print(f"Map File {filename} not found")
        return [], []
    
def pixel_to_tile(px, py, tile_size):
    return int(px // tile_size), int(py // tile_size)


def has_line_of_sight(start_px, end_px, tilemap, tile_size):
    x0, y0 = start_px
    x1, y1=  end_px
    tx0, ty0 = pixel_to_tile(x0, y0, tile_size)
    tx1, ty1 = pixel_to_tile(x1, y1, tile_size)
    dx = tx1 - tx0
    dy = ty1 - ty0

    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return True
    
    step_x = dx / steps
    step_y = dy / steps

    x, y = x0, y0

    for _ in range(steps):
        if y < 0 or y >= len(tilemap) or x < 0 or x >= len(tilemap[0]):
            return False

        if tilemap[int(y)][int(x)] == 1:
            return False
        
        x += step_x
        y += step_y
    return True


tiles, tilemap = load_map("map1.json", TILE_SIZE)

player = Player(200,200)
enemies = [
    Enemy(225,877),
    Enemy(1650, 243),
    Enemy(1510, 588)
]

running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                player.shoot(mouse_pos)

    for tile in tiles:
        pygame.draw.rect(screen, (100,100,100), tile)

    player_pos = Vector2(player.rect.centerx, player.rect.centery)
    for enemy in enemies:
        enemy.update(player_pos, tiles)
        enemy.draw(screen) 
        can_see_player = has_line_of_sight(enemy.rect.center, player.rect.center, tilemap, TILE_SIZE)
        if can_see_player:
            enemy.update(player_pos, tiles)    

        pygame.draw.line(screen, (0,255,0) if can_see_player else (255,0,0), enemy.rect.center, player.rect.center, 2)

    player.move()
    player.update(tiles, enemies, (screen_width, screen_height))
    player.draw(screen, font)

    alive_enemies = sum(1 for e in enemies if not e.dead)
    enemy_text = font.render(f"Enemies: {alive_enemies}/{len(enemies)}", True, (255,255,255))
    screen.blit(enemy_text, (10,100))
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
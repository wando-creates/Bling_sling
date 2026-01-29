import pygame
import json
from player import *

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
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
    

tiles, tilemap = load_map("map1.json", TILE_SIZE)

player = Player(200,200)
enemies = [
    Enemy(500,300),
    Enemy(800, 400),
    Enemy(300, 600)
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

    player.move()
    player.update(tiles, enemies)
    player.draw(screen)

    alive_enemies = sum(1 for e in enemies if not e.dead)
    enemy_text = font.render(f"Enemies: {alive_enemies}/{len(enemies)}", True, (255,255,255))
    screen.blit(enemy_text, (10,100))
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
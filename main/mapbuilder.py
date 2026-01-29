import pygame
import json
pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_width(), screen.get_height()
TILE_SIZE = 50
GRID_WIDTH, GRID_HEIGHT = screen_width // TILE_SIZE, screen_height // TILE_SIZE
MAP_FILE = "map1.json"
clock = pygame.time.Clock()

tilemap = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
mouse_down = False
paint_tile = 1

def save_map():
    with open(MAP_FILE, "w") as f:
        json.dump(tilemap, f)

def draw_grid():
    for x in range(0, screen_width, TILE_SIZE):
        pygame.draw.line(screen, (200,200,200), (x,0), (x,screen_height))
    for y in range(0, screen_height, TILE_SIZE):
        pygame.draw.line(screen, (200,200,200), (0,y), (screen_width, y))

def draw_tiles():
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            if tile == 1:
                rect_x = x * TILE_SIZE
                rect_y = y * TILE_SIZE 
                pygame.draw.rect(screen, (100,100,100), (rect_x, rect_y, TILE_SIZE, TILE_SIZE))

running = True
while running:
    clock.tick(60)
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_F5:
                save_map()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        
    if mouse_down:
        mx, my = pygame.mouse.get_pos()
        grid_x = mx // TILE_SIZE
        grid_y = my // TILE_SIZE

        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            tilemap[grid_y][grid_x] = paint_tile
    
    draw_tiles()
    draw_grid()
    pygame.display.flip()
pygame.quit()
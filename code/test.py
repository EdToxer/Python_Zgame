import pygame

# Initialize game setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Camera variables
camera_pos = pygame.math.Vector2(400, 300)
zoom_level = 2.0  # Higher value = camera is closer

# Mock game object (World space)
obj_world_pos = pygame.math.Vector2(450, 350)
obj_size = 500

# Create a sample surface to represent a sprite
sprite_surf = pygame.Surface((obj_size, obj_size))
sprite_surf.fill((255, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((255, 255, 255))
    
    # --- CAMERA ZOOM LOGIC ---
    # 1. Find position relative to the camera focus
    rel_x = obj_world_pos.x - camera_pos.x
    rel_y = obj_world_pos.y - camera_pos.y
    
    # 2. Scale the relative positions and apply screen center offset
    screen_x = (rel_x * zoom_level) + (800 / 2)
    screen_y = (rel_y * zoom_level) + (600 / 2)
    
    # 3. Scale the visual size of the asset
    scaled_size = int(obj_size * zoom_level)
    scaled_surf = pygame.transform.scale(sprite_surf, (scaled_size, scaled_size))
    
    # 4. Render to screen
    screen.blit(scaled_surf, (screen_x, screen_y))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

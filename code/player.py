from settings import *
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join("images", "Player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(0, 0)

        self.direction = pygame.Vector2()
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 200
        self.collision_sprites = collision_sprites

        self.health = 100
        self.invulnerable_cooldown = 500
        self.invulnerable_time = 0
        self.invulnerable = False

    def load_images(self):
        self.frames = {'left':[], 'right':[], 'up':[], 'down':[]}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        
        if self.direction != pygame.Vector2(0, 0):
            self.direction = self.direction.normalize()

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
        
    def get_bitten(self):
        if not self.invulnerable:
            self.health -= 10
            print(self.health)
            if self.health == 0:
                return True
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
        return False
        
    def invulnerable_timer(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_time >= self.invulnerable_cooldown:
                self.invulnerable = False

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, dt):
        #state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y  != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        #animation
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        #self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.invulnerable_timer()
        self.input()
        self.move(dt)
        self.animate(dt)


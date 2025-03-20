from settings import *

class Enemies(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.frame_index = 0
        self.image = pygame.image.load(join('5games-main', 'Vampire survivor', 'images', 'enemies', 'bat', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = [pygame.image.load(join("5games-main", "Vampire survivor", "images", "enemies", "bat", f'{i}.png')).convert_alpha() for i in range(4)]

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) or keys[pygame.K_d] - int(keys[pygame.K_LEFT]) or keys[pygame.K_a]
        self.direction.y = int(keys[pygame.K_DOWN]) or keys[pygame.K_s] - int(keys[pygame.K_UP]) or keys[pygame.K_w]
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                
    def animate(self, dt):            
        # animate
        self.frame_index += 5 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        
    def update(self, dt):
        # self.input()
        # self.move(dt)
        self.animate(dt)
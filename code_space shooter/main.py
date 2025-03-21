import pygame, random, keyboard, time
from pathlib import Path
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 100

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        # mask
        self.mask = pygame.mask.from_surface(self.image)      
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
 
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] - int(keys[pygame.K_LEFT]))
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            self.laser = Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)  
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5),1)
        self.speed = random.randint(40, 50)  
        self.rotation_speed = random.randint(40, 80)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill() 
        
        # continuous rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.position = pos
    
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:  
            self.kill()

def collision():
    global killed
    global game_active

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        player.kill()
        AnimatedExplosion(explosion_frames, player.rect.center, all_sprites)
        damage_sound.play()
        game_active = False
        killed = True

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score(c_time):
    text_surf = font.render(str(c_time), True, '#ff0055')
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, 'red', text_rect.inflate(20, 10).move(0, -8), 5, 10)
    display_surface.blit(text_surf, text_rect)

def display_start():
    start_surf = font.render('START', True, '#ff0055')
    start_rect = start_surf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, 'red', start_rect.inflate(20, 10).move(0, -8), 5, 10)
    display_surface.blit(start_surf, start_rect)

    return start_rect

def game_over():
    text_surf = font.render("GAME OVER", True, '#ff0055')
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    pygame.draw.rect(display_surface, 'red', text_rect.inflate(20, 10).move(0, -8), 5, 10)
    display_surface.blit(text_surf, text_rect)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display_title = pygame.display.set_caption("Space Shooter")
icon = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
pygame.display.set_icon(icon)
running = True
game_active = False
killed = False
clock = pygame.time.Clock()

# import
star_surf = pygame.image.load(join("5games-main", "space shooter", "images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
explosion_frames = [pygame.image.load(join("5games-main", "space shooter", "images", "explosion", f'{i}.png')).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('5games-main', 'space shooter', 'images', 'Oxanium-Bold.ttf'), 40)

laser_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "laser.wav"))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "explosion.wav"))
damage_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "damage.ogg"))
game_music = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "game_music.wav"))
game_music.set_volume(0.5)
game_music.play(loops= -1)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)

player = Player(all_sprites)

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = 0

    if not game_active:
        start_btn = display_start()
        player.can_shoot = False
        
        if killed:
            game_over()
            all_sprites.empty()
            all_sprites = pygame.sprite.Group()
            meteor_sprites = pygame.sprite.Group()
            player = Player(all_sprites)
            for i in range(20):
                Star(all_sprites, star_surf)                 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and start_btn.collidepoint(event.pos):
                game_active = True
                killed = False
                start_time = pygame.time.get_ticks()
                
        pygame.display.update()      
    else:
        dt = clock.tick() / 300
        player.can_shoot = True
        current_time = (pygame.time.get_ticks() - start_time) // 100

        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == meteor_event:
                x, y = random.randint(0 ,WINDOW_WIDTH), random.randint(-200, -100)
                Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

        #update
        all_sprites.update(dt)
        collision()
        display_score(current_time)

        pygame.display.update()

    #draw the game
    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface)

pygame.quit()
from settings import *
from player import Player
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire survivor")
        pygame.display.set_icon(pygame.image.load(join('5games-main', 'Vampire survivor', 'images', 'enemies', 'bat', '0.png')).convert_alpha())
        self.clock = pygame.time.Clock()
        self.running = True
        self.dead = False
        self.lifes = 3

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 150)
        self.spawn_positions = []

        # font
        self.font = pygame.font.Font(join('5games-main', 'Vampire survivor', 'images', 'Oxanium-Bold.ttf'), 40)
        
        # audio
        self.shoot_sound = pygame.mixer.Sound(join('5games-main', 'Vampire survivor', 'audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.5)
        self.impact_sound = pygame.mixer.Sound(join('5games-main', 'Vampire survivor', 'audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('5games-main', 'Vampire survivor', 'audio', 'music.wav'))
        self.music.set_volume(0.8)
        self.music.play(loops= -1)

        # setup
        self.load_images()
        self.setup()
    
    def load_life(self, life):
        self.life = life
        self.life_surf = self.font.render(f'LIFES: {self.life}', True, '#ff0055')
        self.life_rect = self.life_surf.get_frect(topleft = (15, 20))
        pygame.draw.rect(self.display_surface, 'red', self.life_rect.inflate(20, 10).move(0, -8), 5, 10)
        self.display_surface.blit(self.life_surf, self.life_rect)
    
    def load_restart(self):
        self.restart_surf = self.font.render("RESTART", True, '#ff0055')
        self.restart_rect = self.restart_surf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        pygame.draw.rect(self.display_surface, 'red', self.restart_rect.inflate(20, 10).move(0, -8), 5, 10)
        self.display_surface.blit(self.restart_surf, self.restart_rect)
        pygame.display.update()
    
    def lifes_change(self):
        self.lifes = 3
        self.life = 3

        if self.life > 0:
            self.lifes -= 1
            self.life -= 1
        
        return self.lifes
    
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('5games-main', 'Vampire survivor', 'images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('5games-main', 'Vampire survivor', 'images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('5games-main', 'Vampire survivor', 'images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))    
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join('5games-main', 'Vampire survivor', 'data', 'maps', 'world.tmx'))
        
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.lifes = self.lifes_change()
            self.dead = True
            # self.running = False

    def run(self):
        while self.running:
            # dt
            dt = 0

            if self.dead:
                self.load_restart()
                pygame.display.update()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)
            
            else:
                dt = self.clock.tick() / 1000

                for event in pygame.event.get():
                    if event.type == self.enemy_event:
                        Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)
                # update
                self.gun_timer()
                self.input()
                self.all_sprites.update(dt)
                self.bullet_collision()
                self.player_collision()

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)

            # load health bar
            self.load_life(self.lifes)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
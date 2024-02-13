import pygame, sys, random


class Ship(pygame.sprite.Sprite):
    
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(file='project/graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=(window_width / 2, window_height / 2))
        self.mask = pygame.mask.from_surface(surface=self.image)
        
        self.can_shoot = True
        self.shoot_time = None
        
        self.laser_sound = pygame.mixer.Sound(file='project/sounds/laser.ogg')
        
        pygame.mouse.set_visible(False)
        
    def input_position(self):
        self.rect.center = pygame.mouse.get_pos()
    
    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
            Laser(groups=lasers_group, pos=(self.rect.midtop))
            self.laser_sound.play()
    
    def laser_timer(self, duration=500):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.shoot_time > duration:
                self.can_shoot = True
    
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteors_group, False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()
    
    def update(self):
        self.input_position()
        self.laser_shoot()
        self.laser_timer()
        self.meteor_collision()
        

class Laser(pygame.sprite.Sprite):
    
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pygame.image.load(file='project/graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(surface=self.image)
        
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600
        
        self.explosion_sound = pygame.mixer.Sound(file='project/sounds/explosion.wav')
    
    def meteor_sollision(self):
        if pygame.sprite.groupcollide(lasers_group, meteors_group, True, True, pygame.sprite.collide_mask):
            self.explosion_sound.play()
    
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        if self.rect.bottom < 0:
            self.kill()
        
        self.meteor_sollision()


class Meteor(pygame.sprite.Sprite):
    
    def __init__(self, groups):
        super().__init__(groups)
        meteor_surf = pygame.image.load(file='project/graphics/meteor.png').convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * random.uniform(0.5, 1.5)
        self.scaled_meteor = pygame.transform.scale(surface=meteor_surf, size=meteor_size)
        self.image = self.scaled_meteor
        self.rect = self.image.get_rect(center=(window_width / 2, window_height / 2))
        self.mask = pygame.mask.from_surface(surface=self.image)
        
        self.pos = pygame.math.Vector2(random.randint(-100, window_width + 100), random.randint(-100, -50))
        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 650)
        
        self.rotation = 0
        self.rotation_speed = random.randint(20, 50)
    
    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(surface=self.scaled_meteor, angle=self.rotation, scale=1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(surface=self.image)
        
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rotate()
        
        if self.rect.top > window_height:
            self.kill()


class Score:
    
    def __init__(self):
        self.font = pygame.font.Font(filename='project/graphics/subatomic.ttf', size=50)
        
    def display(self):
        score_text = f'Score: {pygame.time.get_ticks() // 1000}'
        score_surf = self.font.render(text=score_text, antialias=True, color=(255, 255, 255))
        score_rect = score_surf.get_rect(midbottom=(window_width / 2, window_height - 80))
        screen.blit(source=score_surf, dest=score_rect)
        
        pygame.draw.rect(
            surface=screen, 
            color=(255, 255, 255), 
            rect=score_rect.inflate(20, 20), 
            width=5, 
            border_radius=5
        )


# setup the game
pygame.init()

window_width, window_height = 1280, 720
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Spaceship shooter')
clock = pygame.time.Clock()

# background
background_surf = pygame.image.load(file='project/graphics/background.png').convert()

# groups
spaceship_group = pygame.sprite.GroupSingle()
lasers_group = pygame.sprite.Group()
meteors_group = pygame.sprite.Group()

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(event=meteor_timer, millis=500)

# create objects
ship = Ship(groups=spaceship_group)
score = Score()

# music
bg_music = pygame.mixer.Sound(file='project/sounds/music.wav')
bg_music.play(loops=-1)

while True:
    
    # events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == meteor_timer:
            Meteor(groups=meteors_group)
            
    # framerate
    dt = clock.tick() / 1000
    
    # background
    screen.blit(source=background_surf, dest=(0, 0))
    
    # updates
    spaceship_group.update()
    lasers_group.update()
    meteors_group.update()
    
    # graphics
    score.display()
    
    lasers_group.draw(surface=screen)
    spaceship_group.draw(surface=screen)
    meteors_group.draw(surface=screen)
    
    # update the frame
    pygame.display.update()
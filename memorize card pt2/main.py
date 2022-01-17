import pygame, cv2, random, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x ,y) :
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('./images/cards/' + filename)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update(self):
        pass


class Game():
    def __init__(self):
        self.level = 1
        self.level_complete =  False
        self.cards = []
        # get all cards
        self.all_cards = [f for f in os.listdir('./images/cards') if os.path.join('./images/cards', f)]
        
        self.first_lvl = False

        self.img_width, self.img_height = (120,120)
        self.padding = 150
        self.margin_top = WINDOW_HEIGHT // 5
        self.cols = 2
        self.rows = 1
        self.width = WINDOW_WIDTH

        self.tiles_group = pygame.sprite.Group()

        # timing
        self.block_game = False
        self.frame_count = 0

        # generat first leve
        self.generate_level(self.level)


        # Initialize Music
        self.playing_music = True
        self.play_music = pygame.image.load('./images/speaker.png').convert_alpha()
        self.pause_music = pygame.image.load('./images/mute.png').convert_alpha()
        
        self.music_toggle = self.play_music
        self.music_toggle_rect = self.music_toggle.get_rect(topright = (WINDOW_WIDTH - 10, 10))

        # Initialize Video
        self.playing_video = True
        self.play_video = pygame.image.load('./images/play.png').convert_alpha()
        self.stop_video = pygame.image.load('./images/stop.png').convert_alpha()
        
        self.video_toggle = self.play_video
        self.video_toggle_rect = self.video_toggle.get_rect(topright = (WINDOW_WIDTH - 50, 10))
        self.get_video()

        # Load Music
        pygame.mixer.music.load('sounds/bg-music.mp3')
        pygame.mixer.music.set_volume(.0)
        pygame.mixer.music.play()
        

    def update(self, event_list):
        if self.playing_video:
            self.success, self.img = self.capture_video.read()
        
        self.user_inputs(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def draw(self):
        screen.fill(BLACK)

        #fonts
        title_font = pygame.font.Font('./fonts/Little Alien.ttf',44)
        content_font = pygame.font.Font('./fonts/Little Alien.ttf',24)

        #text
        title_text = title_font.render('Memory Game', True, WHITE)
        title_rect = title_text.get_rect(midtop = (WINDOW_WIDTH //2, 10))

        level_text = content_font.render('Level '+str(self.level), True, WHITE )
        level_rect = level_text.get_rect(midtop = (WINDOW_WIDTH //2, 80))

        info_text = content_font.render('Find New ObJect', True, WHITE)
        info_rect = info_text.get_rect(midtop = (WINDOW_WIDTH //2, 120))

        if  self.level == 1:
            next_text = content_font.render('Memorize and find the new object', True, WHITE)
        elif self.first_lvl == True:
            next_text = content_font.render('You Lose, Press Space To Play Again', True, WHITE)
        elif not self.level == 5:
            next_text = content_font.render('Level complete. Press Space for next level', True, WHITE)
        else:
            next_text = content_font.render('Congrats. You Won. Press Space to play again', True, WHITE)
        
        if self.level == 1:
            self.block_game = True
            next_rect = next_text.get_rect(midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 ))
            
            start_text = content_font.render('Press Space for next level', True,WHITE,)
            start_rect = start_text.get_rect(midbottom = (WINDOW_WIDTH//2, WINDOW_HEIGHT //2 + 50))
            

        else:
            next_rect = next_text.get_rect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100 ))


        if self.playing_video:
            if self.success:
                screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'),(0,0))
            else:
                self.get_video()
        else:
            screen.blit(pygame.image.frombuffer(self.img.tobytes(), self.shape, 'BGR'),(0,0))
    

        # Show In The Screen
        if self.level == 1:
            screen.blit(start_text,start_rect) 
        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        screen.blit(self.music_toggle, self.music_toggle_rect)
        screen.blit(self.video_toggle, self.video_toggle_rect)

        # Draw Tilest
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete or self.level == 1:
            screen.blit(next_text, next_rect)
            if self.level ==1:
                self.level_complete = True

    def generate_tileset(self, cards):
        self.cols = self.rows = self.cols if self.cols <= self.rows else self.rows
        TILES_WIDTH = (self.img_width * self.cols + self.padding )
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2.3
        
        self.tiles_group.empty()

        for i in range(len(cards)):
          
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.cols * (self.img_height + self.padding))
         
            tile = Tile(cards[i], x, y)
            self.tiles_group.add(tile)

    def user_inputs(self,event_list):
        for event in event_list:
            # Music Toggle Controller
            if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 :
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.playing_music:
                        self.playing_music = False
                        self.music_toggle = self.pause_music
                        pygame.mixer.music.pause()
                    else:
                        self.playing_music= True
                        self.music_toggle = self.play_music
                        pygame.mixer.music.unpause()

                # video Toggle Controller
                if self.video_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.playing_video:
                        self.playing_video = False
                        self.video_toggle = self.stop_video
                    else:
                        self.playing_video = True
                        self.video_toggle = self.play_video
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 12 or self.first_lvl == True:
                        self.level = 1
                    self.block_game = False
                    self.first_lvl = False
                    self.generate_level(self.level)

    def generate_level(self,level):
        self.cards = self.all_cards[:level+1]
        self.cards_random = random.sample(self.cards,len(self.cards))
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 3
        self.generate_tileset(self.cards_random)
    
    def get_video(self):
        self.capture_video = cv2.VideoCapture('./video/Full_Frame.mp4')
        self.success, self.img= self.capture_video.read()
        self.shape = self.img.shape[1::-1]            

    def check_level_complete(self,event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            if tile.name == self.cards[-1].split('.')[0]:

                                effect = pygame.mixer.Sound('sounds/win.wav')
                                effect.play()
                                self.level_complete = True
                                self.block_game = True
                                
                            else:
                                self.block_game = True
                                effect = pygame.mixer.Sound('sounds/lose.wav')
                                effect.play()
                                self.level_complete = True
                                self.first_lvl = True
                                
                                
        else:
            self.frame_count +=1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False
               
                # self.generate_level(self.level)                       

pygame.init()

# set constant variables
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WHITE = (255, 255, 255)
PURPLE = (128, 212, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Memory Card Game')

# creat new objct of the game
game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
    game.update(event_list)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
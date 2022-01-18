import pygame, os,random
from pygame.locals import *

class Player():
    def __init__(self, parent_screen):
        self.screen = parent_screen
        self.player_right = pygame.image.load('./images/icons/player_right.png').convert_alpha()
        self.player_left = pygame.image.load('./images/icons/player_left.png').convert_alpha()
        self.player = self.player_right
        self.x = 500
        self.y = 500
        self.direction = ''
        self.speed = 10

    def go_right(self):
        self.direction = 'right'
        # self.player = self.player_right
    
    def go_left(self):
        self.direction = 'left'
        self.player = self.player_left
    
    def go_up(self):
        self.direction = 'up'
    
    def go_down(self):
        self.direction = 'down'

    def run(self):
        if self.direction == 'right':
            self.x += self.speed
        if self.direction == 'left':
            self.x -= self.speed
        if self.direction == 'up':
            self.y -= self.speed
        if self.direction == 'down':
            self.y += self.speed

        self.draw()

    def draw(self):
        self.screen.blit(self.player,(self.x, self.y))
        pygame.display.flip()

class Game():
    def __init__(self):
        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080
        self.BROWN = (122, 122, 82)
        self.BLACK = (0,0,0)
        self.BLUE = (102, 194, 255)
        self.FSDOKY = (254, 247, 219)
        self.START = True
        self.HOLY_GAME = True
        self.STOP_GAME = False

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('EXPLORE EGYPT GAME')

        #load fonts
        self.h1_italic_font = pygame.font.Font('./fonts/LobsterTwo-BoldItalic.ttf',60)
        self.h2_italic_font = pygame.font.Font('./fonts/LobsterTwo-Italic.ttf',50)
        self.content_font = pygame.font.Font('./fonts/LobsterTwo-Bold.ttf',23)

        #load game's class
        self.player = Player(self.screen)
   
    def render_start_Page(self, start):
        if start:
            # set background
            self.back_image = pygame.image.load('./images/background/back2.png').convert_alpha()
            
            #set start icon
            self.play_button = pygame.image.load('./images/icons/play3.png').convert_alpha()
            self.play_button_rect = self.play_button.get_rect(midbottom=(self.WINDOW_WIDTH//2,self.WINDOW_HEIGHT-150))
            
            #set start text
            self.head_text = self.h1_italic_font.render('WELCOME TO EXPLORE EGYPT GAME', True, self.BROWN)
            self.head_text_rect = self.head_text.get_rect(midleft=(490,100))
            self.bottom_text = self.h2_italic_font.render("Let's Explore Together", True, self.BROWN)
            self.bottom_text_rect = self.bottom_text.get_rect(midleft=(750,170))

            # render start's screen
            self.screen.blit(self.back_image,(0,0))
            self.screen.blit(self.play_button,self.play_button_rect)
            self.screen.blit(self.head_text,self.head_text_rect)
            self.screen.blit(self.bottom_text,self.bottom_text_rect)
            pygame.display.flip()
        else:
            self.render_whole_Game()
    
    def render_whole_Game(self):
        self.screen.fill(self.FSDOKY)
        self.back_image = pygame.image.load('./images/background/back3.png').convert_alpha()
        self.image = pygame.image.load('./images/background/shape1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(100,100))
        self.screen.blit(self.image,self.rect)
        # self.screen.blit(self.back_image,(0,-400))
        pygame.display.flip()
    
    def play(self):
        self.render_start_Page(self.START)
        if not self.START and self.HOLY_GAME:
            self.render_whole_Game()
            self.HOLY_GAME = False
        self.player.run()
            

    def user_inputs(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                    if self.play_button_rect.collidepoint(pygame.mouse.get_pos()) and self.START:
                        self.START = False

                if event.type == pygame.KEYDOWN and not self.STOP_GAME:
                    if event.key == pygame.K_LEFT:
                        self.player.go_left()
                    
                    if event.key == pygame.K_RIGHT:
                        self.player.go_right()

                    if event.key == pygame.K_UP:
                        self.player.go_up()
                    
                    if event.key == pygame.K_DOWN:
                        self.player.go_down()
                self.play()
       
pygame.init() 
game = Game()
game.user_inputs()

pygame.quit()
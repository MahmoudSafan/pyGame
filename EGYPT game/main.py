import pygame, os,time,random

class Game():
    def __init__(self):
        pygame.init()  
        
        self.WINDOW_WIDTH = 1920
        self.WINDOW_HEIGHT = 1080
        self.BROWN = (122, 122, 82)
        self.START = True

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('EXPLORE EGYPT GAME')

        #load fonts
        self.h1_italic_font = pygame.font.Font('./fonts/LobsterTwo-BoldItalic.ttf',60)
        self.h2_italic_font = pygame.font.Font('./fonts/LobsterTwo-Italic.ttf',50)
        self.content_font = pygame.font.Font('./fonts/LobsterTwo-Bold.ttf',23)

    def play(self,event_list):
       self.render_start_Page(self.START)
       self.user_inputs(event_list)

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

    def user_inputs(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    print('start')


       

    game = Game()
    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            else:
                game.play(event_list)
        pygame.display.update()


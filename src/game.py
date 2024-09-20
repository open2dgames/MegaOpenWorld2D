import pygame
import pytmx 
import pyscroll
import pytmx.util_pygame
from player import Player
from map import MapManager

class Game: 
    def __init__(self):
        # creer la fenetre du jeu 
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Pygamon - Aventure")

        # generer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
    

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()

    
    def update(self):
        self.map_manager.update()


    def run(self):
        clock = pygame.time.Clock()

        # boucle du jeu 
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60) # Bride à 60 FPS

        pygame.quit()
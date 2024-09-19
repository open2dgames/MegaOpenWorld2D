import pygame
import pytmx 
import pyscroll
import pytmx.util_pygame
from player import Player

class Game: 
    def __init__(self):
        # creer la fenetre du jeu 
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Pygamon - Aventure")

        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('map/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # definir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4) # ICI LE DEFAULT LAYER
        self.group.add(self.player)

        # definir le rect de collision pour entrer dans la maison
        enter_zone = tmx_data.get_object_by_name('enter_zone')
        self.enter_zone_rect = pygame.Rect(enter_zone.x, enter_zone.y, enter_zone.width, enter_zone.height)

        # definir le monde où se trouve le joueur
        self.map = 'world'

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')

        if pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')

        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

        if pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')

    def switch_zone(self):
        # charger la zone (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('map/zone1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # definir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4) # ICI LE DEFAULT LAYER
        self.group.add(self.player)

        # definir le rect de collision pour entrer dans la maison
        enter_zone = tmx_data.get_object_by_name('exit_zone') # Ici bien changé le enter_zone pour que le joueur ne reste pas bloquer dans ce monde éternellement
        self.enter_zone_rect = pygame.Rect(enter_zone.x, enter_zone.y, enter_zone.width, enter_zone.height)

        # récuperer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_zone')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y

    def switch_world(self):
                # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('map/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # definir une liste qui va stocker les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4) # ICI LE DEFAULT LAYER
        self.group.add(self.player)

        # definir le rect de collision pour entrer dans la maison
        enter_zone = tmx_data.get_object_by_name('enter_zone') # Ici bien changé le enter_zone pour que le joueur ne reste pas bloquer dans ce monde éternellement
        self.enter_zone_rect = pygame.Rect(enter_zone.x, enter_zone.y, enter_zone.width, enter_zone.height)

        # récuperer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_zone_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y

    def update(self):
        self.group.update()

        # vérifier l'entrée dans la zone 1
        if  self.map == 'world' and self.player.feet.colliderect(self.enter_zone_rect):
            self.switch_zone()
            self.map = 'zone1'

        # vérifier l'entrer dans le monde 
        if self.map == 'zone1' and self.player.feet.colliderect(self.enter_zone_rect):
            self.switch_world()
            self.map = 'world'

        # verification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()

        # boucle du jeu 
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60) # Bride à 60 FPS

        pygame.quit()
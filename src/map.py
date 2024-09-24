from dataclasses import dataclass
import pygame, pytmx, pyscroll
from player import NPC

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:

    def __init__(self, screen, player):
        self.maps = dict() # un dictionnaire pour les plusieurs maps accessibles via des clés, PEUT ETRE: faire un script avec des strucs pour les clés
        self.screen = screen
        self.player = player
        self.current_map = "carte"

        self.register_map("carte", portals=[
            Portal(from_world="carte", origin_point="enter_zone", target_world="zone1", teleport_point="spawn_zone"),
            Portal(from_world="carte", origin_point="enter_zone2", target_world="zone2", teleport_point="spawn_point"),
            Portal(from_world="carte", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon")
        ], npcs=[
            NPC("paul", nb_points=4, dialog=["bonne aventure", "je m'appelle Paul"])
        ])
        
        self.register_map("zone1", portals=[
            Portal(from_world="zone1", origin_point="exit_zone", target_world="carte", teleport_point="enter_zone_exit")
        ])

        self.register_map("zone2", portals=[
            Portal(from_world="zone2", origin_point="exit_zone2", target_world="carte", teleport_point="exit_zone2")
        ], npcs=[
            NPC("robin", nb_points=2, dialog=["Salutation", "je m'appelle Robin"])
        ])

        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="carte", teleport_point="dungeon_exit_spawn")
        ], npcs=[
            NPC("boss", nb_points=2, dialog=["HAHA", "Ohio Final BOSS"])
        ])

        self.teleport_player("player")
        self.teleport_npcs()

    def check_npc_collisions(self, dialog_box):
        collide_with_npc = False
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)
                collide_with_npc = True
        
        if not collide_with_npc:
            dialog_box.quit_dialog()

        

    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f"map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # definir une liste qui va stocker les rectangles de collision
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4) # ICI LE DEFAULT LAYER
        group.add(self.player)

        # recuperer tout les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Creer un objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self): 
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()

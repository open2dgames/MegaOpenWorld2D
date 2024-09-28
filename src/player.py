import pygame
from animation import AnimateSprite
import math

class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)

        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()
    
    # Refactoriser le système de mouvement pour qu'il n'y ait qu'une fonction concise (utiliser des vecteurs)(good luck pour les anim)
    def move_right(self): 
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self): 
        self.change_animation("left")
        self.position[0] -= self.speed

    def move_up(self): 
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self): 
        self.change_animation("down")
        self.position[1] += self.speed

    
    def move(self, x, y):
        length = math.sqrt(x**2 + y**2)

        # Éviter le mouvement diagonal si le vecteur n'est pas nul
        if length > 0:            
            # Appliquer la vitesse
            self.position[0] += (x * self.speed) / length
            self.position[1] += (y * self.speed)/ length
        
        if y == 1:
            self.change_animation("down")

        if y == -1:
            self.change_animation("up")

        if x == -1:
            self.change_animation("left")
            
        if x == 1:
            self.change_animation("right")


    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    def move_back(self, i=None): 

        if i == None : self.position = self.old_position
        else : self.position[i] = self.old_position[i]
        
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_to_pos(self, position):
        self.position = position

        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    
class Player(Entity):
    
    def __init__(self):
        super().__init__("player", 0, 0)

class NPC(Entity):

    def __init__(self, name, nb_points, dialog):
        super().__init__(name, 0, 0) 
        self.nb_points = nb_points
        self.dialog = dialog
        self.speed = 1
        self.points = []
        self.name = name
        self.current_point = 0

    # Better systeme of movement towards a point
    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


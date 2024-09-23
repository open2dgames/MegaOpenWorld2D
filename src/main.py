import pygame

from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

# Road to finish part 2 du tutoriel de Graven
# - les animations, passage derrière les arbres, dialogues

# Pouvoir ajouter des maps sans passer par le code
# Faire une documentation en béton pour les beginners
# Changer le code pour que les portails fonctionnent sans référencement dans le code (avec des boucles objects et des names spécifiques)
# pareil pour les npcs (et leurs déplacement sans référencement) (pour rendre le process rapide et faisable directement dans Tiled)
# Régler le système de mouvement du joueur (diag)  
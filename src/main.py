import pygame
import sys
from game import Game
from modules.Button import Button


game = Game()


def menu():

    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    WIDTH, HEIGHT = 800, 600
    WIDTHB, HEIGHTB = 150, 50
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu com Botão Aumentando")

    
    font = pygame.font.Font(None, 150)
    text = font.render("TANK", 1, WHITE)

    play = Button(WIDTH // 2 - 80, HEIGHT // 2 , WIDTHB, HEIGHTB, "PLAY", 20, WHITE, RED, BLACK, SCREEN)
    credit = Button(WIDTH // 2 - 80, HEIGHT // 2 + 60, WIDTHB, HEIGHTB, "CREDITS", 20, WHITE, RED, BLACK, SCREEN)
    exit = Button(WIDTH // 2 - 80, HEIGHT // 2 + 120, WIDTHB, HEIGHTB, "EXIT", 20, WHITE, RED, BLACK, SCREEN)



        

    clock = pygame.time.Clock()

    while True:
        SCREEN.fill(BLACK)
        SCREEN.blit(text, (WIDTH // 2 - 140, HEIGHT // 2 - 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.clicked(pygame.mouse.get_pos()):
                    game.play()
                elif credit.clicked(pygame.mouse.get_pos()):
                    SCREEN.fill(BLACK)
                    font = pygame.font.Font(None, 36)
                    text = font.render("Developers: ", 1, WHITE)
                        
                    SCREEN.blit(text, (WIDTH // 2 - 140, HEIGHT // 2 - 200))
                    pygame.display.flip()
                else:
                    pygame.quit()

        play.draw(pygame.mouse.get_pos())
        credit.draw(pygame.mouse.get_pos())
        exit.draw(pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    menu()

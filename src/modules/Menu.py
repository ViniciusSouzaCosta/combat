import pygame
import sys

from modules.Button import Button1



class Menu:
    def menu(inicialize):

        # Inicialização do Pygame
        pygame.init()

        # Definição das cores
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        # Definição das dimensões da janela
        WIDTH, HEIGHT = 800, 600
        WIDTHB, HEIGHTB = 150, 50
        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Menu com Botão Aumentando")

        # Criação do botão
        play = Button1(WIDTH // 2 - 80, HEIGHT // 2 , WIDTHB, HEIGHTB, "PLAY", 20, WHITE, RED, BLACK, SCREEN)
        credit = Button1(WIDTH // 2 - 80, HEIGHT // 2 + 60, WIDTHB, HEIGHTB, "CREDITS", 20, WHITE, RED, BLACK, SCREEN)
        exit = Button1(WIDTH // 2 - 80, HEIGHT // 2 + 120, WIDTHB, HEIGHTB, "EXIT", 20, WHITE, RED, BLACK, SCREEN)

        

        clock = pygame.time.Clock()

        while True:
            SCREEN.fill(BLACK)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play.clicked(pygame.mouse.get_pos()):
                        inicialize
                      
                        credits.BreakoutGame()
                    elif credit.clicked(pygame.mouse.get_pos()):
                        SCREEN.fill(BLACK)
                        font = pygame.font.Font(None, 36)
                        text = font.render("Developers: ", 1, WHITE)
                        
                        SCREEN.blit(text, (WIDTH // 2 - 140, HEIGHT // 2 - 200))
                        pygame.display.flip()
                    else:
                        pygame.quit()

            # Desenhar o botão
            play.draw(pygame.mouse.get_pos())
            credit.draw(pygame.mouse.get_pos())
            exit.draw(pygame.mouse.get_pos())

            pygame.display.flip()
            clock.tick(60)


    if __name__ == "__menu__":
        menu()


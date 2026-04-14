import pygame
import player
import sys

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)


player.init_player()
player.load_song()

def draw():
    screen.fill((255, 255, 255))

    text = font.render(f"Now playing: {player.get_current_song()}", True, (0, 0, 0))
    screen.blit(text, (50, 150))

    pygame.display.flip()


running = True
while running:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_song()

            elif event.key == pygame.K_b:
                player.prev_song()

            elif event.key == pygame.K_q:
                running = False

pygame.quit()
sys.exit()
import pygame
import sys
import ga

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Game Loop")
clock = pygame.time.Clock()

running = True
while running:
    # 1. EVENT LOOP (Same as SDL_PollEvent)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. CLEAR SCREEN (Fill with dark grey)
    screen.fill((30, 30, 30))

    # 3. DRAW STUFF (Equivalent to SDL_RenderLines/Geometry)
    # Target, Color (RGB), Center (X, Y), Radius, Width (0 means filled)
    pygame.draw.circle(screen, (255, 0, 0), (250, 300), 100)          # Filled Red
    pygame.draw.circle(screen, (255, 255, 255), (550, 300), 100, 2)   # White Outline
    if len(sys.argv)>1:
        pygame.draw.circle(screen, (255, 255, 255), (250, 300), 100, 2)   # White Outline

    # 4. PRESENT (Same as SDL_RenderPresent)
    pygame.display.flip()

    # Limit to 60 FPS
    clock.tick(60)

pygame.quit()
sys.exit()
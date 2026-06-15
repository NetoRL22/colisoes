import sys
import ga
import fisica
import render

# Initialize Pygame
fisica.setup(sys.argv[1])
render.setup()

running = True
while running:
    # 1. EVENT LOOP (Same as SDL_PollEvent)
    for event in render.pygame.event.get():
        if event.type == render.pygame.QUIT:
            running = False

    # 2. CLEAR SCREEN (Fill with dark grey)
    render.screen.fill((30, 30, 30))

    # 3. DRAW STUFF (Equivalent to SDL_RenderLines/Geometry)
    # Target, Color (RGB), Center (X, Y), Radius, Width (0 means filled)
    ### pygame.draw.circle(screen, (255, 0, 0), (250, 300), 100)          # Filled Red
    ### pygame.draw.circle(screen, (255, 255, 255), (550, 300), 100, 2)   # White Outline
    ### if len(sys.argv)>1:
    ###     pygame.draw.circle(screen, (255, 255, 255), (250, 300), 100, 2)   # White Outline
    fisica.colidirBolas()
    fisica.atualizaV()
    fisica.atualizaPos()
    if(fisica.threeD):
        render.desenhaQuinas()
    render.ordenaRend()
    render.projetaPosicoes()
    render.projetaRaios()
    render.desenhaBolas()
    fisica.calculaStats()
    render.printaStats()

    # 4. PRESENT (Same as SDL_RenderPresent)
    render.pygame.display.flip()

    # Limit to 60 FPS
    render.clock.tick(fisica.tps)

render.pygame.quit()
sys.exit()
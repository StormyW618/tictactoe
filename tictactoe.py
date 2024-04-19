import pygame

#setup
pygame.init()
height = 800
width = 800
screen = pygame.display.set_mode((width, height))
running = True
WHITE = (255,255,255)

while running:
      
   #drawing board test
    
        
    pygame.draw.line(screen, WHITE, [width / 3, 0], [width / 3, height])
    pygame.draw.line(screen, WHITE, [width / 3 * 2, 0], [width / 3 * 2, height])
    
    pygame.draw.line(screen, WHITE, [0, height / 3], [width, height / 3])
    pygame.draw.line(screen, WHITE, [0, height / 3 * 2], [width, height / 3 * 2])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()

pygame.quit()

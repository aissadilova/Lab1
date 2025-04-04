import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rectangle Drawing Tool")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Drawing variables
LMBpressed = False
THICKNESS = 5
prevx, prevy = 0, 0  # Start position
currx, curry = 0, 0  # Current position

# Create base layer for persistent drawing
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(WHITE)

def calculate_rect(x1, y1, x2, y2):
    """Calculate rectangle coordinates from any two points"""
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def main():
    global LMBpressed, THICKNESS, prevx, prevy, currx, curry
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("LMB pressed!")
                LMBpressed = True
                prevx, prevy = event.pos
                currx, curry = event.pos
            
            # Mouse motion
            if event.type == pygame.MOUSEMOTION:
                print("Mouse position:", event.pos)
                if LMBpressed:
                    currx, curry = event.pos
                    # Refresh screen with base layer
                    screen.blit(base_layer, (0, 0))
                    # Draw current rectangle
                    rect = calculate_rect(prevx, prevy, currx, curry)
                    pygame.draw.rect(screen, RED, rect, THICKNESS)
            
            # Mouse button up
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                print("LMB released!")
                LMBpressed = False
                currx, curry = event.pos
                # Draw final rectangle to base layer
                rect = calculate_rect(prevx, prevy, currx, curry)
                pygame.draw.rect(base_layer, RED, rect, THICKNESS)
                # Refresh screen
                screen.blit(base_layer, (0, 0))
            
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    print("Increased thickness")
                    THICKNESS += 1
                elif event.key == pygame.K_MINUS:
                    print("Reduced thickness")
                    THICKNESS = max(1, THICKNESS - 1)
        
        # Display update
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
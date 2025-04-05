"""
Enhanced Paint Application with Geometric Shapes

This program extends the basic rectangle drawing tool to include multiple geometric shapes.
Users can draw squares, right triangles, equilateral triangles, rhombuses, and rectangles.
The application features persistent drawing, adjustable line thickness, and on-screen instructions.

Controls:
- Click and drag to draw shapes
- 1-5 keys to select shape type
- +/- keys to adjust line thickness
"""

import pygame
import sys
import math

# Initialize pygame library
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Drawing Tool")

# Color definitions (RGB values)
WHITE = (255, 255, 255)  # Background color
RED = (255, 0, 0)        # Drawing color
BLACK = (0, 0, 0)        # Text color

# Drawing state variables
LMBpressed = False       # Track if left mouse button is pressed
THICKNESS = 5            # Current drawing line thickness
prevx, prevy = 0, 0      # Start position of current shape
currx, curry = 0, 0      # Current mouse position
current_shape = "rectangle"  # Currently selected shape

# Create base layer for persistent drawing (stores all completed shapes)
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(WHITE)  # Start with white background

def calculate_rect(x1, y1, x2, y2):
    """
    Calculate rectangle coordinates from any two diagonal points.
    
    Args:
        x1, y1: First point coordinates
        x2, y2: Second point coordinates
    
    Returns:
        pygame.Rect object representing the rectangle
    """
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def calculate_square(x1, y1, x2, y2):
    """
    Calculate square coordinates from any two points.
    Uses the smaller dimension to maintain equal sides.
    
    Args:
        x1, y1: First point coordinates
        x2, y2: Second point coordinates
    
    Returns:
        pygame.Rect object representing the square
    """
    size = min(abs(x1 - x2), abs(y1 - y2))  # Ensure equal width and height
    return pygame.Rect(min(x1, x2), min(y1, y2), size, size)

def calculate_right_triangle(x1, y1, x2, y2):
    """
    Calculate points for a right triangle with the right angle at the starting point.
    
    Args:
        x1, y1: Right angle point coordinates
        x2, y2: Opposite corner coordinates
    
    Returns:
        List of three points (tuples) forming the triangle
    """
    return [(x1, y1), (x1, y2), (x2, y2)]

def calculate_equilateral_triangle(x1, y1, x2, y2):
    """
    Calculate points for an equilateral triangle (all sides equal).
    The base is along the x-axis from the starting point.
    
    Args:
        x1, y1: First base point coordinates
        x2, y2: Second base point coordinates
    
    Returns:
        List of three points (tuples) forming the triangle
    """
    base = x2 - x1
    height = (math.sqrt(3) / 2) * abs(base)  # Equilateral triangle height formula
    
    # Calculate apex position
    apex_x = x1 + base/2
    if y2 > y1:
        apex_y = y1 - height  # Draw upward
    else:
        apex_y = y1 + height  # Draw downward
    
    return [(x1, y1), (x2, y1), (apex_x, apex_y)]

def calculate_rhombus(x1, y1, x2, y2):
    """
    Calculate points for a rhombus (diamond shape).
    The shape is centered between the two points.
    
    Args:
        x1, y1: First corner coordinates
        x2, y2: Opposite corner coordinates
    
    Returns:
        List of four points (tuples) forming the rhombus
    """
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return [
        (center_x, y1),  # Top point
        (x2, center_y),  # Right point
        (center_x, y2),  # Bottom point
        (x1, center_y)   # Left point
    ]

def draw_current_shape(surface, color, x1, y1, x2, y2, thickness):
    """
    Draw the currently selected shape based on user's choice.
    
    Args:
        surface: Pygame surface to draw on
        color: Color of the shape
        x1, y1: Start coordinates
        x2, y2: End coordinates
        thickness: Line thickness for the shape
    """
    if current_shape == "rectangle":
        rect = calculate_rect(x1, y1, x2, y2)
        pygame.draw.rect(surface, color, rect, thickness)
    elif current_shape == "square":
        rect = calculate_square(x1, y1, x2, y2)
        pygame.draw.rect(surface, color, rect, thickness)
    elif current_shape == "right_triangle":
        points = calculate_right_triangle(x1, y1, x2, y2)
        pygame.draw.polygon(surface, color, points, thickness)
    elif current_shape == "equilateral_triangle":
        points = calculate_equilateral_triangle(x1, y1, x2, y2)
        pygame.draw.polygon(surface, color, points, thickness)
    elif current_shape == "rhombus":
        points = calculate_rhombus(x1, y1, x2, y2)
        pygame.draw.polygon(surface, color, points, thickness)

def display_instructions():
    """
    Display the control instructions on screen.
    Shows current shape and thickness information.
    """
    font = pygame.font.SysFont(None, 24)
    instructions = [
        "1: Rectangle  2: Square  3: Right Triangle",
        "4: Equilateral Triangle  5: Rhombus",
        "+/-: Change thickness",
        f"Current: {current_shape.replace('_', ' ').title()}, Thickness: {THICKNESS}"
    ]
    
    # Draw semi-transparent background for instructions
    s = pygame.Surface((WIDTH, 80), pygame.SRCALPHA)
    s.fill((255, 255, 255, 128))  # White with 50% transparency
    screen.blit(s, (0, 0))
    
    # Render each line of instructions
    for i, line in enumerate(instructions):
        text = font.render(line, True, BLACK)
        screen.blit(text, (10, 10 + i * 25))

def main():
    """
    Main application loop.
    Handles user input and coordinates drawing operations.
    """
    global LMBpressed, THICKNESS, prevx, prevy, currx, curry, current_shape
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse button down - start drawing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                LMBpressed = True
                prevx, prevy = event.pos  # Store starting position
                currx, curry = event.pos
            
            # Mouse motion - update current shape preview
            if event.type == pygame.MOUSEMOTION:
                if LMBpressed:
                    currx, curry = event.pos
                    # Refresh screen with base layer
                    screen.blit(base_layer, (0, 0))
                    # Draw current shape preview
                    draw_current_shape(screen, RED, prevx, prevy, currx, curry, THICKNESS)
            
            # Mouse button up - finalize shape
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                LMBpressed = False
                currx, curry = event.pos
                # Draw final shape to base layer
                draw_current_shape(base_layer, RED, prevx, prevy, currx, curry, THICKNESS)
                # Refresh screen
                screen.blit(base_layer, (0, 0))
            
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                # Thickness control
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    THICKNESS += 1
                elif event.key == pygame.K_MINUS:
                    THICKNESS = max(1, THICKNESS - 1)  # Don't go below 1
                
                # Shape selection
                elif event.key == pygame.K_1:
                    current_shape = "rectangle"
                elif event.key == pygame.K_2:
                    current_shape = "square"
                elif event.key == pygame.K_3:
                    current_shape = "right_triangle"
                elif event.key == pygame.K_4:
                    current_shape = "equilateral_triangle"
                elif event.key == pygame.K_5:
                    current_shape = "rhombus"
        
        # Display instructions
        display_instructions()
        
        # Update the display
        pygame.display.flip()
    
    # Clean up pygame and exit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
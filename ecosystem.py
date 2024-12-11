import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Virtual Ecosystem Simulation")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Slider settings
slider_width, slider_height = 150, 20
tree_growth_slider_rect = pygame.Rect(10, 10, slider_width, slider_height)
recycling_slider_rect = pygame.Rect(10, 40, slider_width, slider_height)
pollution_slider_rect = pygame.Rect(width - slider_width - 200, 10, slider_width, slider_height)
animal_population_slider_rect = pygame.Rect(width - slider_width - 200, 40, slider_width, slider_height)

# Initial slider values
pollution_level = 50
tree_growth_rate = 50
animal_population = 50
recycling_rate = 50

# Ecosystem parameters
pollution = 50

# Font settings
font = pygame.font.Font(None, 24)

# Simulation speed
clock = pygame.time.Clock()

# Generate initial positions for trees
tree_positions = [(random.randint(200, width), random.randint(100, height)) for _ in range(tree_growth_rate)]

# Generate initial positions for animals
animal_positions = [(random.randint(200, width), random.randint(100, height)) for _ in range(animal_population)]

# Function to draw sliders
def draw_slider(slider_rect, value, max_value=100):
    pygame.draw.rect(window, BLACK, slider_rect, 2)
    fill_rect = slider_rect.copy()
    fill_rect.width = int(slider_rect.width * (value / max_value))
    pygame.draw.rect(window, GREEN, fill_rect)

# Function to draw labels
def draw_label(text, pos):
    label = font.render(text, True, BLACK)
    window.blit(label, pos)

# Function to draw a tree
def draw_tree(position):
    trunk_width, trunk_height = 5, 15
    foliage_radius = 10
    trunk_rect = pygame.Rect(position[0] - trunk_width // 2, position[1] - trunk_height, trunk_width, trunk_height)
    pygame.draw.rect(window, BROWN, trunk_rect)
    pygame.draw.circle(window, GREEN, (position[0], position[1] - trunk_height), foliage_radius)

# Function to move animals slowly
def move_animals():
    for i in range(len(animal_positions)):
        x, y = animal_positions[i]
        x += random.choice([-1, 0, 1])
        y += random.choice([-1, 0, 1])
        animal_positions[i] = (x, y)

# Function to adjust pollution based on tree count and recycling rate
def adjust_pollution(tree_growth_rate, recycling_rate):
    global pollution

    if tree_growth_rate > 70 and recycling_rate > 70:
        pollution = max(0, pollution - 0.1)  # Both are high, pollution decreases
    elif tree_growth_rate > 50 and recycling_rate > 50:
        pollution = max(0, pollution - 0.05)  # Both are moderately high, pollution decreases slowly
    elif tree_growth_rate > 30 and recycling_rate > 30:
        pollution = max(0, pollution - 0.02)  # Both are average, pollution decreases very slowly
    elif tree_growth_rate < 30 and recycling_rate < 30:
        pollution = min(100, pollution + 0.1)  # Both are low, pollution increases
    elif tree_growth_rate < 30 or recycling_rate < 30:
        pollution = min(100, pollution + 0.05)  # One is low, pollution increases slowly
    elif (tree_growth_rate >= 15 and tree_growth_rate <= 30 and recycling_rate > 50) or (recycling_rate >= 15 and recycling_rate <= 30 and tree_growth_rate > 50):
        pollution = max(0, pollution - 0.02)  # One is moderately low and the other is high, pollution decreases very slowly
    elif (tree_growth_rate > 30 and recycling_rate > 30):
        pollution = max(0, pollution - 0.02)  # Both are above 30, pollution decreases very slowly

# Call this function in the adjust_ecosystem function
def adjust_ecosystem():
    global animal_population, tree_growth_rate, recycling_rate
    
    # Adjust animal population based on tree count
    if abs(tree_growth_rate - animal_population) > 2:
        if animal_population > tree_growth_rate:
            animal_population -= 0.1  # Decrease animal population slowly
        elif animal_population < tree_growth_rate:
            animal_population += 0.1  # Increase animal population slowly

    # Adjust pollution based on tree count and recycling rate
    adjust_pollution(tree_growth_rate, recycling_rate)
    
    # Update animal positions based on current animal population
    while len(animal_positions) < int(animal_population):
        animal_positions.append((random.randint(200, width), random.randint(100, height)))
    while len(animal_positions) > int(animal_population):
        animal_positions.pop()

# Function to draw a smiley face
def draw_smiley(pollution):
    face_center = (60, 250)
    face_radius = 30

    # Define face colors for different moods
    HAPPY_COLOR = (255, 255, 0)
    SMILING_COLOR = (255, 255, 102)
    SOBER_COLOR = (255, 204, 102)
    UNHAPPY_COLOR = (255, 153, 102)
    VERY_SAD_COLOR = (255, 102, 102)

    # Set face color based on pollution level
    if pollution <= 10:
        face_color = HAPPY_COLOR
    elif 10 < pollution <= 30:
        face_color = SMILING_COLOR
    elif 30 < pollution <= 50:
        face_color = SOBER_COLOR
    elif 50 < pollution <= 70:
        face_color = UNHAPPY_COLOR
    else:
        face_color = VERY_SAD_COLOR

    # Draw face
    pygame.draw.circle(window, face_color, face_center, face_radius)
    pygame.draw.circle(window, BLACK, (face_center[0] - 10, face_center[1] - 10), 5)  # Left eye
    pygame.draw.circle(window, BLACK, (face_center[0] + 10, face_center[1] - 10), 5)  # Right eye

    # Draw mouth based on pollution level
    if pollution <= 10:
        pygame.draw.arc(window, BLACK, (face_center[0] - 15, face_center[1] - 5, 30, 20), 3.14, 0, 2)  # Happy
    elif 10 < pollution <= 30:
        pygame.draw.arc(window, BLACK, (face_center[0] - 15, face_center[1], 30, 20), 3.14, 0, 2)  # Smiling
    elif 30 < pollution <= 50:
        pygame.draw.line(window, BLACK, (face_center[0] - 15, face_center[1] + 10), (face_center[0] + 15, face_center[1] + 10), 2)  # Sober
    elif 50 < pollution <= 70:
        pygame.draw.arc(window, BLACK, (face_center[0] - 15, face_center[1] + 10, 30, 20), 0, 3.14, 2)  # Unhappy
    else:
        pygame.draw.arc(window, BLACK, (face_center[0] - 15, face_center[1] + 15, 30, 20), 0, 3.14, 2)  # Very sad


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if tree_growth_slider_rect.collidepoint(event.pos):
                new_tree_growth_rate = int((event.pos[0] - tree_growth_slider_rect.x) / slider_width * 100)
                if new_tree_growth_rate > tree_growth_rate:
                    additional_trees = new_tree_growth_rate - tree_growth_rate
                    tree_positions.extend([(random.randint(200, width), random.randint(100, height)) for _ in range(additional_trees)])
                elif new_tree_growth_rate < tree_growth_rate:
                    reduced_trees = tree_growth_rate - new_tree_growth_rate
                    tree_positions = tree_positions[:-reduced_trees]
                tree_growth_rate = new_tree_growth_rate
            elif recycling_slider_rect.collidepoint(event.pos):
                recycling_rate = int((event.pos[0] - recycling_slider_rect.x) / slider_width * 100)
            elif pollution_slider_rect.collidepoint(event.pos):
                pollution_level = int((event.pos[0] - pollution_slider_rect.x) / slider_width * 100)
            elif animal_population_slider_rect.collidepoint(event.pos):
                animal_population = int((event.pos[0] - animal_population_slider_rect.x) / slider_width * 100)
    
    # Update simulation based on slider values
    pollution_level = int(pollution)
    
    # Move animals slowly
    move_animals()
    
    # Gradually adjust ecosystem based on tree count and recycling rate
    adjust_ecosystem()
    
    # Clear screen
    window.fill(WHITE)

    # Draw ecosystem elements
    for pos in tree_positions:
        draw_tree(pos)
    for pos in animal_positions:
        pygame.draw.circle(window, BLUE, pos, 5)
    
    # Draw pollution overlay
    pollution_overlay = pygame.Surface((width, height))
    pollution_overlay.set_alpha(int(pollution * 2.3))  # Adjust transparency based on pollution level
    pollution_overlay.fill(BROWN)
    window.blit(pollution_overlay, (0, 0))

    # Draw sliders
    draw_slider(tree_growth_slider_rect, tree_growth_rate)
    draw_slider(recycling_slider_rect, recycling_rate)
    draw_slider(pollution_slider_rect, pollution_level)
    draw_slider(animal_population_slider_rect, int(animal_population))

    # Draw slider labels
    draw_label(f"Tree Growth Rate: {tree_growth_rate}", (170, 10))
    draw_label(f"Recycling Rate: {recycling_rate}", (170, 40))
    draw_label(f"Pollution Level: {int(pollution)}", (width - 190, 10))
    draw_label(f"Animal Population: {int(animal_population)}", (width - 190, 40))

    # Draw legend
    draw_label("Legend:", (10, 80))
    trunk_width, trunk_height = 5, 15
    position = [30, 130]
    trunk_rect = pygame.Rect(position[0] - trunk_width // 2, position[1] - trunk_height, trunk_width, trunk_height)
    pygame.draw.rect(window, BROWN, trunk_rect)
    pygame.draw.circle(window, GREEN, (position[0], position[1] - trunk_height), 8)
    draw_label("Trees", (50, 115))
    pygame.draw.circle(window, BLUE, (30, 150), 5)
    draw_label("Animals", (50, 145))

    # Draw smiley face based on pollution level
    draw_smiley(pollution)

    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(10)  # Slower frame rate to reduce speed of animal movement

pygame.quit()
try:
    sys.exit()
except SystemExit:
    pass

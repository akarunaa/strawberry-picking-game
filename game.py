import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
PINK = (255, 105, 180)  # Default pink color for player

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Strawberry Picking Game")

# Fonts
font = pygame.font.Font("Inter-Regular.ttf", 38)
medium_font = pygame.font.Font("Inter-Regular.ttf", 36)
small_font = pygame.font.Font("Inter-Regular.ttf", 28)


# Game states
START_SCREEN = 0
GAMEPLAY_SCREEN = 1
GAME_OVER_SCREEN = 2
game_state = START_SCREEN  # Initially, we are at the start screen

# Load images
background_image = pygame.image.load('background.png')  # Make sure to use the correct path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit screen

player_image = pygame.image.load('player.png')  # Replace with your player image path
player_image = pygame.transform.scale(player_image, (100, 100))  # Resize player image

strawberry_image = pygame.image.load('strawberry.png')  # Replace with your strawberry image path
strawberry_image = pygame.transform.scale(strawberry_image, (30, 30))  # Resize strawberry

# Game variables
player_x = SCREEN_WIDTH // 2 - 25
player_y = 420  # Start position for player
player_vel = 5
jumping = False
on_ledge = False
velocity_y = 0  # Y-axis velocity (for smooth jumping)
jump_height = -10  # Initial jump speed (negative for upwards)
gravity = 0.5  # Gravity effect for falling
jump_count = 0  # Track the number of jumps
strawberries_collected = 0  # Track the number of strawberries collected

strawberries = []

# Game over flag
game_over = False

# Clock for frame rate
clock = pygame.time.Clock()

# Timer variables
time_left = 30  # Time limit for the game in seconds
timer_started = False  # Flag to check if the timer has started

# Draw start screen
def draw_start_screen():
    screen.fill(WHITE)
    welcome_text = font.render("Welcome to Strawberry Picking Adventure! ", True, PINK)
    screen.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, 100))  # Position at top
    # Render the instructions
    instructions_text = small_font.render("Use arrow keys to move and space to jump!", True, PINK)
    screen.blit(instructions_text, (
    SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))  # Below the start text

    # Render the "Can you collect all the strawberries before time runs out?" text
    time_text = small_font.render("Can you collect all the strawberries before time runs out?", True, PINK)
    screen.blit(time_text,
                (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))  # Below the instructions

    text = medium_font.render("Press Enter to Start", True, PINK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

# Draw gameplay screen
def draw_gameplay_screen():
    screen.blit(background_image, (0, 0))  # Draw the background image

    # Draw strawberries
    for strawberry in strawberries:
        screen.blit(strawberry_image, strawberry.topleft)  # Draw strawberries

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw timer
    timer_text = small_font.render(f"Time: {time_left}", True, PINK)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))  # Display timer in the top-right corner

    # Draw strawberries collected count
    strawberries_text = small_font.render(f"Strawberries Collected: {strawberries_collected}", True, PINK)
    screen.blit(strawberries_text, (10, 10))  # Display the count at the top-left corner

    pygame.display.update()

# Draw game over screen
def draw_game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over!", True, PINK)
    play_again_text = small_font.render("Press 'Y' to Play Again or 'N' to Quit", True, PINK)

    screen.blit(game_over_text, (
    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()

# Handle collisions between the player and strawberries
def handle_collisions():
    global player_x, player_y, jumping, game_over, jump_count, velocity_y, on_ledge, strawberries_collected

    player_rect = pygame.Rect(player_x, player_y, 50, 50)

    # Apply gravity only if the player is not on the ground (or ledge)
    if not on_ledge:
        velocity_y += gravity  # Apply gravity
        player_y += velocity_y  # Update player position based on velocity

        # Prevent player from falling below a certain level (ground level)
        if player_y >= 432:  # Ground level at Y = 400
            player_y = 432  # Lock the player at ground level
            velocity_y = 0  # Reset velocity when landing
            jump_count = 0  # Reset jump count
            on_ledge = False  # Ensure on_ledge is reset when landing

    # Handle jumping
    if jumping and velocity_y != 0:
        velocity_y += gravity  # Apply gravity continuously to simulate jump arc
        player_y += velocity_y  # Update player's vertical position during jump

        # Check for strawberry collection
        for strawberry in strawberries[:]:
            if player_rect.colliderect(strawberry):
                strawberries.remove(strawberry)  # Collect strawberry
                strawberries_collected += 1  # Increment the strawberry count
                break

# Reset the game
def reset_game():
    global player_x, player_y, strawberries, time_left, timer_started, strawberries_collected
    # Reset player position
    player_x = 400  # Fixed X position for player
    player_y = 400  # Fixed Y position for player
    strawberries.clear()  # Clear any existing strawberries
    strawberries_collected = 0  # Reset strawberries collected count

    # Generate new strawberries
    for _ in range(20):  # Generate 20 strawberries
        strawberry_x = random.randint(50, SCREEN_WIDTH - 50)
        strawberry_y = random.randint(50, SCREEN_HEIGHT - 50)
        strawberry_y = random.randint(50, 419)
        strawberry = pygame.Rect(strawberry_x, strawberry_y, 30, 30)
        strawberries.append(strawberry)

    time_left = 30  # Reset the timer
    timer_started = False  # Reset timer start flag

# Main game loop
def game_loop():
    global player_x, game_state, player_y, jumping, game_over, on_ledge, jump_count, velocity_y, time_left, timer_started, strawberries_collected

    last_time = pygame.time.get_ticks()  # Store the current time in milliseconds

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == START_SCREEN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = GAMEPLAY_SCREEN  # Switch to the gameplay screen when Enter is pressed
                    reset_game()  # Ensure strawberries are generated when the game starts

            if game_state == GAMEPLAY_SCREEN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_x -= player_vel * 4  # Move left
                    elif event.key == pygame.K_RIGHT:
                        player_x += player_vel * 4  # Move right
                    if event.key == pygame.K_SPACE and not jumping:  # Only jump if not already jumping
                        jumping = True  # Start the jump
                        velocity_y = jump_height  # Set the jump velocity

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        jumping = False  # Stop jumping when spacebar is released

            if game_state == GAME_OVER_SCREEN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  # Play again
                        game_state = GAMEPLAY_SCREEN
                        reset_game()  # Reset game to initial state
                    elif event.key == pygame.K_n:  # Quit game
                        pygame.quit()
                        sys.exit()

        if game_state == START_SCREEN:
            draw_start_screen()  # Draw start screen

        if game_state == GAMEPLAY_SCREEN:
            # Update the timer once every second
            current_time = pygame.time.get_ticks()
            if current_time - last_time >= 1000:  # If 1 second has passed
                last_time = current_time
                if time_left > 0:
                    time_left -= 1  # Decrease timer every second
                else:
                    game_over = True
                    game_state = GAME_OVER_SCREEN  # Switch to game over screen when time is up

            handle_collisions()  # Check for collisions (fall, strawberries)

            draw_gameplay_screen()  # Draw gameplay screen

        if game_state == GAME_OVER_SCREEN:
            draw_game_over_screen()  # Draw game over screen

        clock.tick(60)  # Set game frame rate

if __name__ == "__main__":
    game_loop()  # Run the game loop

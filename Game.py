import pygame, sys, random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

lose_sound = pygame.mixer.Sound("pa0-pa0/assets/Nooo.mp3")
lose_sound.set_volume(0.8)
hit_sound = [  
    pygame.mixer.Sound("pa0-pa0/assets/pinpon.mp3"),
    pygame.mixer.Sound("pa0-pa0/assets/a_pinpon.mp3"),
    pygame.mixer.Sound("pa0-pa0/assets/Cerdo.mp3"),
    pygame.mixer.Sound("pa0-pa0/assets/Pinoccio.mp3")]

for audio in hit_sound:
    audio.set_volume(0.9)

last_sound = None

def play_random_hit():
    global last_sound
    sound = random.choice(hit_sound)
    while sound == last_sound:
        sound = random.choice(hit_sound)
    sound.play()
    last_sound = sound

def ball_movement():
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, start

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 8
    if start:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False

    # Ball collision with the player paddle
    if ball.colliderect(player):
        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle
            # TODO Task 2: Fix score to increase by 1
            score += 1  # Increase player score
            ball_speed_y *= -1  # Reverse ball's vertical direction
            # TODO Task 6: Add sound effects HERE
            play_random_hit()


    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        pygame.mixer.music.stop()
        lose_sound.play()
        restart()  # Reset the game

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    speed = 9
    global ball_speed_x, ball_speed_y, score

    ball.center = (screen_width / 2, screen_height / 2)  # Reset ball position to center
    score = 0  # Reset player score
    ball_speed_x = speed * random.choice((-1, 1))  # Randomize initial horizontal direction
    ball_speed_y = speed * random.choice((-1, 1))

    # Reiniciar música
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)

# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shrek The Game')  # Set window title
pygame.mixer.music.load("pa0-pa0/assets/Believer_arreglada.mp3")
# Se añadió la música en bucle, all final sale el cantante de smash mouth diciendo algo. Pensé en quitarlo pero env como homenaje lo voy a dejar.
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)


# Background
background = pygame.image.load("pa0-pa0/assets/Shrek bg.png")#Imagen de Shrek
pygame.transform.scale(background, (screen_height, screen_width))
bg_color = pygame.Color('grey12')

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 75, 75)  # Tamaño de la bola
shrek_img = pygame.image.load("pa0-pa0/assets/shrek_face.png").convert_alpha()
shrek_img = pygame.transform.smoothscale(shrek_img, (ball.width, ball.height))


# TODO Task 1 Make the paddle bigger
player_height = 15
player_width = 125
player = pygame.Rect(screen_width/2 - 45, screen_height - 20, player_width, player_height)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

# Score Text setup
score = 0
basic_font = pygame.font.Font('pa0-pa0/assets/Prince Valiant.ttf', 50)  # Font for displaying score

start = True  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Luis Añeses"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 10  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 10  # Move paddle right
            if event.key == pygame.K_SPACE:
                start = True  # Start the ball movement
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 10  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 10  # Stop moving right

    # Game Logic
    ball_movement()
    player_movement()

    # Visuals
    light_grey = pygame.Color('grey83')
    red = pygame.Color('red')
    screen.fill(bg_color)  # Clear screen with background color
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, red, player)  # Draw player paddle
    green = pygame.Color("green") # TODO Task 3: La bola es de color verde ahora
    screen.blit(shrek_img, ball) # Draw ball
    player_text = basic_font.render(f'{score}', False, red)  # Render player score
    screen.blit(player_text, (screen_width/2 - 15, 10))  # Display score on screen

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 frames per second


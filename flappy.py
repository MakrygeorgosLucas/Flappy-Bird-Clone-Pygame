import random
import sys
import pygame
from pygame.locals import *

"""
Defining global variables for the game
"""
FPS = 32
# defining the screen size
screen_width = 289
screen_hight = 511
# defining the window of the game
window = pygame.display.set_mode((screen_width, screen_hight))
# reduce the screen hight to have place for the "base(.png)"
# so if the bird touches the base its over
play_area = screen_hight * 0.8
# defining the game image
game_image = {}
# defining the game audio
game_audio_sound = {}
# defining the player
player = 'images/bird.png'
# defining the background
background_image = 'images/background.png'
# defining the obstacle
pipe_image = 'images/pipe-green.png'


def welcome_main_screen():
    """
    this function is going to show the welcome screen to the user
    until he presses something
    """
    # we define the x and y coordinates
    p_x = int(screen_width / 5)
    p_y = int(screen_hight - game_image['player'].get_height() / 2)

    # for the message we have 2 functions:
    # 1 on the x and one on the y coordinates
    msg_x = int((screen_width - game_image['message'].get_width()) / 2)
    msg_y = int(screen_hight * 0.13)

    # for the base we only need the x coordinate
    b_x = 0

    while True:
        for event in pygame.event.get():
            # if the user clicks on the cross button it closes the game
            # "K_ ... " = Key
            # ex :  K_SPACE  = the space button on the keyboard
            if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if the player wants to start the game
            elif event.type == KEYDOWN and (
                    event.key == K_SPACE or event.key == K_UP):
                return
            else:
                # window.blit is responsible for displaying the background,
                # player, message, and base images on the game window
                # during each iteration of the game loop.
                window.blit(game_image['background'], (0, 0))
                window.blit(game_image['player'], (p_x, p_y))
                window.blit(game_image['message'], (msg_x, msg_y))
                window.blit(game_image['base'], (b_x, play_area))
                # updates the contents of the entire display window, refreshing
                # it to reflect any changes made during the game loop
                pygame.display.update()
                # this ensures that the game loop runs at a specified (FPS)
                # (Frame Per Second)
                time_clock.tick(FPS)


def main_gameplay():
    """
    this function is the code for the main gameplay
    """
    score = 0

    # spicify the x and y coordinates for the player
    p_x = int(screen_width / 5)
    p_y = int(screen_width / 2)
    b_x = 0

    # specify the coordinates for the pipes
    n_pipe1 = get_Random_Pipes()
    n_pipe2 = get_Random_Pipes()

    # defining the coodrinates of pipes and addig 200 pixels between them
    # n_pipe1 is a list with dictionarys , si the n_pipe[0]['y'] means
    # the first dicitonary from the list and the 'y' key from it
    up_pipes = [
        {'x': screen_width + 200, 'y': n_pipe1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': n_pipe2[0]['y']}
    ]

    down_pipes = [
        {'x': screen_width + 200, 'y': n_pipe1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': n_pipe2[1]['y']}
    ]

    # pipe vertical speed
    pipe_Vx = -4

    # player vertical speed (gravity)
    p_vx = -9

    # player move speed
    p_mvx = 10
    p_mvy = -8

    # player accuracy
    p_accuracy = 1

    # flapp accuracy (the speed that the bird is gonna move up when flapping)
    p_flap_accuracy = -8
    p_flap = False

    # gaming loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user clicks space or key up the game starts
            elif event.type == KEYDOWN and (
                    event.key == K_SPACE or event.key == K_UP):
                if p_y > 0:
                    p_vx = p_flap_accuracy
                    p_flap = True
                    game_audio_sound['wing'].play()

        # collision test (to check if the bird is colliding with the pipes)
        cl_test = is_Colliding(p_x, p_y, up_pipes, down_pipes)
        if cl_test:
            return

        # variable for the middle position of the player
        p_middle_position = p_x + game_image['player'].get_width() / 2
        for pipe in up_pipes:
            # variable for the pipe middle position
            pipe_middle_position = pipe['x'] + game_image['pipe'][
                0].get_width() / 2
            # if the player has passed the middle position of the pipe gets a point
            if pipe_middle_position <= p_middle_position < pipe_middle_position + 4:
                score += 1
                print(f"Your Score is {score}")
                game_audio_sound['point'].play()

        # the down speed of the bird increases , the game gets harder
        if p_vx < p_mvx and not p_flap:
            p_vx += p_accuracy

        if p_flap:
            p_flap = False
        # to get the height of the player
        p_height = game_image['player'].get_height()
        # to change the y coordinate
        p_y = p_y + min(p_vx, play_area - p_y - p_height)

        # the up pipes and low pipes coorditanes is going to change
        # at the start the pipes have 200 distance between them and this
        # for loop descreases the distance between every next pipe
        for pipe_upper, pipe_lower in zip(up_pipes, down_pipes):
            pipe_upper['x'] += pipe_Vx
            pipe_lower['x'] += pipe_Vx

        #  Check if the leading edge of the first upper pipe is about to enter
        #  the game window
        if 0 < up_pipes[0]['x'] < 5:
            # Generate a new set of pipes and add them to the game
            new_pipe = get_Random_Pipes()
            up_pipes.append(new_pipe[0])
            down_pipes.append(new_pipe[1])

        # Check if the leading edge of the first upper pipe has moved
        # off the left side of the game window
        if up_pipes[0]['x'] < -game_image['pipe'][0].get_width():
            # Remove the first set of pipes from the list as they are no longer visible
            up_pipes.pop(0)
            down_pipes.pop(0)

        window.blit(game_image['background'], (0, 0))
        # Move each pair of upper and lower pipes towards the left side of the game window
        for pipe_upper, pipe_lower in zip(up_pipes, down_pipes):
            window.blit(game_image['pipe'][0],
                        (pipe_upper['x'], pipe_upper['y']))
            window.blit(game_image['pipe'][1],
                        (pipe_lower['x'], pipe_lower['y']))

        # Draw the base (ground) onto the game window at the current
        # x-coordinate and play_area (bottom of the game window)
        window.blit(game_image['base'], (b_x, play_area))

        # Draw the player character onto the game window at the current x and y coordinates
        window.blit(game_image['player'], (p_x, p_y))

        # Convert the score to a list of individual digits
        d = [int(x) for x in list(str(score))]

        # Calculate the total width needed for displaying the score digits
        w = 0
        for digit in d:
            w += game_image['numbers'][digit].get_width()

        # Calculate the X offset to center the score digits on the screen
        Xoffset = (screen_width - w) / 2

        # Iterate through each digit in the score and draw it onto the screen at the calculated position
        for digit in d:
            window.blit(game_image['numbers'][digit],
                        (Xoffset, screen_hight * 0.12))
            Xoffset += game_image['numbers'][digit].get_width()

        # Update the display to reflect the changes
        pygame.display.update()

        # Control the frame rate of the game by ticking the clock
        time_clock.tick(FPS)


def is_Colliding(p_x, p_y, up_pipes, down_pipes):
    """
    We have 3 options to collide :
        - Hitting the top
        - Hitting the botton
        - Hitting the pipes
    """
    # for hitting the top or the bottom
    if p_y > play_area - 25 or p_y < 0:
        game_audio_sound['hit'].play()
        return True

    # for the pipes
    for pipe in up_pipes:
        # pipe_h gets the up pipe height
        pipe_h = game_image['pipe'][0].get_height()

        # Check if the player's y-coordinate is within the range of the upper pipe
        # and if the player's x-coordinate is close enough to the pipe's x-coordinate
        if (p_y < pipe_h + pipe['y'] and abs(p_x - pipe['x']) <
                game_image['pipe'][0].get_width()):
            # Play the 'hit' sound effect when the player hits a pipe
            game_audio_sound['hit'].play()
            return True

    # for the collision with the lower pipes
    for pipe in down_pipes:

        # Check if the bottom of the player character is below the upper edge of the lower pipe
        # and if the player's x-coordinate is close enough to the lower pipe's x-coordinate
        if (p_y + game_image['player'].get_height() > pipe['y'] and abs(p_x - pipe['x']) <
                game_image['pipe'][0].get_width()):
            game_audio_sound['hit'].play()
            return True


def get_Random_Pipes():
    """
    Generates ranodom positions for the pipes
    """
    # to get the height of the pipe
    pipe_h = game_image['pipe'][0].get_height()

    # to get the surface area of the pipe
    off_s = screen_hight/3

    # to get the y coordinate of the lower pipe (ylp)
    ylp = off_s + random.randrange(0, int(screen_hight - game_image['base'].get_height() - 1.2 * off_s))

    # to get the x coordinate of both pipes
    pipeX = screen_width + 10

    # upper pipe y coordinate
    yup = pipe_h - ylp + off_s

    # specify the coordinates of 2 pipes
    pipe = [
        # upper pipe
        {'x': pipeX, 'y': -yup},
        # lower pipe
        {'x': pipeX, 'y': ylp}
    ]

    return pipe


if __name__ == "__main__":
    # initialize the pygame
    pygame.init()
    # defining time_clock for the game
    time_clock = pygame.time.Clock()
    # set the caption
    pygame.display.set_caption("Flappy Bird Game")
    # load the images and the sounds
    # conver_aplha converts it to an aplha numeric number
    game_image['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )

    game_image['message'] = pygame.image.load(
        'images/message.png').convert_alpha()
    game_image['base'] = pygame.image.load('images/base.png').convert_alpha()

    # we use transform so the pipes have different size
    # and different positions in the game
    game_image['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(),
                                180),
        pygame.image.load(pipe_image).convert_alpha())

    game_audio_sound['die'] = pygame.mixer.Sound('sounds/die.wav')
    game_audio_sound['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    game_audio_sound['point'] = pygame.mixer.Sound('sounds/point.wav')
    game_audio_sound['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    game_audio_sound['wing'] = pygame.mixer.Sound('sounds/wing.wav')

    game_image['background'] = pygame.image.load(background_image).convert()
    game_image['player'] = pygame.image.load(player).convert_alpha()

    while True:
        welcome_main_screen()
        main_gameplay()

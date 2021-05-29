import sys
import os
import pygame
import random

from pygame import time
from player import Player
from ball import Ball
from button import Button

"""
SETUP section - preparing everything before the main loop runs
"""
pygame.init()

# Global constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FRAME_RATE = 60

# Useful colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GREY = (120, 120, 120)

# Creating the screen and the clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(0)  # Make alpha bits transparent
clock = pygame.time.Clock()

background = pygame.image.load("assets/background.jpg").convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


def intro_menu():
    intro_loop = True
    intro_font = pygame.font.Font(None, int(SCREEN_HEIGHT/10))

    # heading text - 1/8
    heading = pygame.font.Font(None, int(SCREEN_HEIGHT/5)).render("Pong - by Divy Patel", True, WHITE)

    # single vs mult player buttons - 3/8
    singlePlayer = Button(WHITE, (SCREEN_WIDTH/3, SCREEN_HEIGHT*(3/8)), intro_font, "1 Player")
    singlePlayer.active = True
    mode = 1
    multiPlayer = Button(WHITE, (SCREEN_WIDTH*(2/3), SCREEN_HEIGHT*(3/8)), intro_font, "2 Player")

    # Points to win input: options - 10, 20, unlimited - 4/8
    fivePoints = Button(WHITE, (SCREEN_WIDTH/4, SCREEN_HEIGHT/2), intro_font, "5 points")
    fivePoints.active = True
    goal = 5
    tenPoints = Button(WHITE, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), intro_font, "10 points")
    unlimitedPoints = Button(WHITE, (SCREEN_WIDTH*(3/4), SCREEN_HEIGHT/2), intro_font, "Unlimited")

    # difficulty button - 5/8
    easyButton = Button(WHITE, (SCREEN_WIDTH*(7/50), SCREEN_HEIGHT*(5/8)), intro_font, "Easy", 225)
    easyButton.active = True
    difficulty = "easy"
    mediumButton = Button(WHITE, (SCREEN_WIDTH*(19/50), SCREEN_HEIGHT*(5/8)), intro_font, "Medium", 225)
    hardButton = Button(WHITE, (SCREEN_WIDTH*(31/50), SCREEN_HEIGHT*(5/8)), intro_font, "Hard", 225)
    impossibleButton = Button(WHITE, (SCREEN_WIDTH*(43/50), SCREEN_HEIGHT*(5/8)), intro_font, "Impossible", 225)

    # play button - 4/5
    play = Button(WHITE, (SCREEN_WIDTH/2, SCREEN_HEIGHT*(4/5)), pygame.font.Font(None, int(SCREEN_HEIGHT/5)), "Play")

    # buttons list
    buttons = (
    singlePlayer, multiPlayer, 
    fivePoints, tenPoints, unlimitedPoints, 
    easyButton, mediumButton, hardButton, impossibleButton, 
    play
    )

    while intro_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # When user clicks the 'x' on the window, close our game
                intro_loop = False
                pygame.quit()
                sys.exit()
        
        # Mouse events
        mouse_pos = pygame.mouse.get_pos()  # Get position of mouse as a tuple representing the
        # (x, y) coordinate
        mouse_buttons = pygame.mouse.get_pressed() # if clicked

        # hover over buttons
        for button in buttons:
            if button.active:
                button.color = LIGHT_GREY
            else:
                button.color = WHITE
            # if mouse clicked on button
            if button.hover(mouse_pos):
                button.color = GREY
                if mouse_buttons[0]:
                    if button == play:
                        main(mode, goal, difficulty)
                    if not button.active:
                        button.active = True
                        
                        # mode
                        if button == singlePlayer:
                            mode = 1
                            multiPlayer.active = False
                        elif button == multiPlayer:
                            mode = 2
                            singlePlayer.active = False
                        
                        # goal
                        if button == fivePoints:
                            goal = 5
                            tenPoints.active = False
                            unlimitedPoints.active = False
                        elif button == tenPoints:
                            goal = 10
                            fivePoints.active = False
                            unlimitedPoints.active = False
                        elif button == unlimitedPoints:
                            goal = 999
                            fivePoints.active = False
                            tenPoints.active = False
                        
                        # difficulty
                        if button == easyButton:
                            difficulty = "easy"
                            mediumButton.active = False
                            hardButton.active = False
                            impossibleButton.active = False
                        elif button == mediumButton:
                            difficulty = "medium"
                            easyButton.active = False
                            hardButton.active = False
                            impossibleButton.active = False
                        elif button == hardButton:
                            difficulty = "hard"
                            easyButton.active = False
                            mediumButton.active = False
                            impossibleButton.active = False
                        elif button == impossibleButton:
                            difficulty = "impossible"
                            easyButton.active = False
                            mediumButton.active = False
                            hardButton.active = False

                        time.wait(300)

        screen.fill(BLACK)  # Fill the screen with one colour
        screen.blit(background, (0,0))
        
        # heading
        screen.blit(heading, (SCREEN_WIDTH/2 - (heading.get_width()/2), SCREEN_HEIGHT/8))

        # single vs multiplayer option button
        singlePlayer.draw(screen, BLACK, 2)
        multiPlayer.draw(screen, BLACK, 2)
        play.draw(screen, BLACK, 2)

        # points buttons
        fivePoints.draw(screen, BLACK, 2)
        tenPoints.draw(screen, BLACK, 2)
        unlimitedPoints.draw(screen, BLACK, 2)

        # difficulty buttons
        easyButton.draw(screen, BLACK, 2)
        mediumButton.draw(screen, BLACK, 2)
        hardButton.draw(screen, BLACK, 2)
        impossibleButton.draw(screen, BLACK, 2)

        pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
        clock.tick(int(FRAME_RATE/4))  # Pause the clock to always maintain FRAME_RATE frames per second


def main(mode, goal, difficulty):
    
    first_frame = True

    # set mode
    if mode == 1:
        one_player = True
    elif mode == 2:
        one_player = False

    # sprites declaration
    players = pygame.sprite.Group()

    player_1 = Player(SCREEN_HEIGHT, SCREEN_WIDTH, (SCREEN_WIDTH - (3*(SCREEN_WIDTH/100)), SCREEN_HEIGHT/2), "Player 1")
    players.add(player_1)
    player_1_text = pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render(str(player_1.name), True, WHITE)

    player_2 = Player(SCREEN_HEIGHT, SCREEN_WIDTH, (3*(SCREEN_WIDTH/100), SCREEN_HEIGHT/2), "Player 2")
    players.add(player_2)
    if mode == 1:
        player_2.name = "Computer"
    player_2_text = pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render(player_2.name, True, WHITE)

    balls = pygame.sprite.Group()
    ball = Ball(SCREEN_HEIGHT, SCREEN_WIDTH)
    balls.add(ball)

    # set difficulty - easy, medium, hard, impossible
    if difficulty == "impossible":
        new_ball_y = impossible(ball)
    else:
        new_ball_y = SCREEN_HEIGHT/2

    # menu button
    menuButton = Button(WHITE, (SCREEN_WIDTH/2, SCREEN_HEIGHT/27), pygame.font.Font(None, int(SCREEN_HEIGHT/10)), "Menu")

    # rally counter
    rally = 0
    rally_text = pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render("Rally: " + str(rally), True, WHITE)

    main_loop = True

    while main_loop:
        """
        EVENTS section - how the code reacts when users do things
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # When user clicks the 'x' on the window, close our game
                main_loop = False
                pygame.quit()
                sys.exit()
            
        # Keyboard events
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] and player_1.rect.top > 0:
            player_1.move(-1)
        if keys_pressed[pygame.K_DOWN] and player_1.rect.bottom < SCREEN_HEIGHT:
            player_1.move(1)
        
        # for two player
        if not one_player and keys_pressed[pygame.K_w] and player_2.rect.top > 0:
            player_2.move(-1)
        if not one_player and keys_pressed[pygame.K_s] and player_2.rect.bottom < SCREEN_HEIGHT:
            player_2.move(1)
        
        # for single player
        if difficulty == "easy":
            easy(ball.rect.center[1], player_2)

        elif difficulty == "medium":
            if ball.rect.x > SCREEN_WIDTH/4:
                easy(ball.rect.center[1], player_2)
            else:
                easy(new_ball_y, player_2)

        elif difficulty == "hard":
            if ball.rect.x > SCREEN_WIDTH/3:
                easy(ball.rect.center[1], player_2)
            else:
                easy(new_ball_y, player_2)

        elif difficulty == "impossible":
            easy(new_ball_y, player_2)

        # Mouse events
        mouse_pos = pygame.mouse.get_pos()  # Get position of mouse as a tuple representing the
        # (x, y) coordinate

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # If left mouse pressed
            pass  # Replace this line
        if mouse_buttons[2]:  # If right mouse pressed
            pass  # Replace this line

        menuButton.color = WHITE
        if menuButton.hover(mouse_pos):
            menuButton.color = GREY
            if mouse_buttons[0]:
                time.wait(200)
                main_loop = False
                intro_menu()

        """
        UPDATE section - manipulate everything on the screen
        """
        if not first_frame:
            balls.update()

        # collision
        collision = pygame.sprite.spritecollide(ball, players, False)
        for player in collision:
            if ball.player_bounce:
                ball.player_bounce = False
                ball.wall_bounce = True
                ball.new_speed(player.rect.center[1], rally)
                rally += 1
                rally_text = pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render("Rally: " + str(rally), True, WHITE)
                if player == player_1:
                    new_ball_y = impossible(ball)
                else:
                    new_ball_y = SCREEN_HEIGHT/2
        
        # score
        if ball.rect.right > SCREEN_WIDTH:
            player_2.score += 1
            rally = 0
            rally_text = pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render("Rally: " + str(rally), True, WHITE)
            time.wait(200)
            first_frame = True
            ball.reset()
            player_1.reset()
            player_2.reset()
            new_ball_y = SCREEN_HEIGHT/2
        
        elif ball.rect.left < 0:
            player_1.score += 1
            rally = 0
            rally_text = pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render("Rally: " + str(rally), True, WHITE)
            time.wait(200)
            first_frame = True
            ball.reset()
            player_1.reset()
            player_2.reset()
            new_ball_y = SCREEN_HEIGHT/2
        

        """
        DRAW section - make everything show up on screen
        """
        screen.fill(BLACK)  # Fill the screen with one colour
        screen.blit(background, (0,0))

        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), 3)

        # player names
        screen.blit(player_1_text, ((SCREEN_WIDTH*(3/4)) - (player_1_text.get_width()/2), SCREEN_HEIGHT*(9/10)))
        screen.blit(player_2_text, ((SCREEN_WIDTH/4) - (player_2_text.get_width()/2), SCREEN_HEIGHT*(9/10)))

        # players
        players.draw(screen)

        # balls
        balls.draw(screen)

        # menu button
        menuButton.draw(screen, BLACK, 2)

        # rally counter
        if rally >= 10:
            screen.blit(rally_text, ((SCREEN_WIDTH/2) - (rally_text.get_width()/2), SCREEN_HEIGHT*(9/10)))

        # score
        screen.blit(pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render(str(player_1.score), True, WHITE), (SCREEN_WIDTH*(3/4), 10))
        screen.blit(pygame.font.Font(None, int(SCREEN_HEIGHT/10)).render(str(player_2.score), True, WHITE), (SCREEN_WIDTH/4, 10))


        pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
        clock.tick(FRAME_RATE)  # Pause the clock to always maintain FRAME_RATE frames per second
        if first_frame:
            time.wait(1000)
            first_frame = False
            for player in [player_1, player_2]:
                if player.score >= goal:
                    gameOver(player_1.score, player_2.score, player.name, player_1.name, player_2.name)
                    main_loop = False
                    break


def gameOver(player_1_score, player_2_score, winner, player_1_name, player_2_name):
    over_loop = True
    over_font = pygame.font.Font(None, int(SCREEN_HEIGHT/10))

    # heading text
    line_1 = pygame.font.Font(None, int(SCREEN_HEIGHT/5)).render("Game Over", True, WHITE)
    line_2 = over_font.render(str(winner) + " wins", True, WHITE)
    line_3 = over_font.render("(-: Score :-)", True, WHITE)

    # score text
    player_1_text = over_font.render(str(player_1_name) + ": " + str(player_1_score), True, WHITE)
    player_2_text = over_font.render(str(player_2_name) + ": " + str(player_2_score), True, WHITE)
    
    # menu button
    menuButton = Button(WHITE, (SCREEN_WIDTH/2, SCREEN_HEIGHT*(7/8)), pygame.font.Font(None, int(SCREEN_HEIGHT/5)), "Menu")

    while over_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # When user clicks the 'x' on the window, close our game
                over_loop = False
                pygame.quit()
                sys.exit()

        # Mouse events
        mouse_pos = pygame.mouse.get_pos()  # Get position of mouse as a tuple representing the
        # (x, y) coordinate
        mouse_buttons = pygame.mouse.get_pressed()

        menuButton.color = WHITE
        if menuButton.hover(mouse_pos):
            menuButton.color = GREY
            if mouse_buttons[0]:
                time.wait(200)
                over_loop = False
                intro_menu()
        
        screen.fill(BLACK)  # Fill the screen with one colour
        screen.blit(background, (0,0))

        # menu button
        menuButton.draw(screen, BLACK, 2)

        screen.blit(line_1, (SCREEN_WIDTH/2 - (line_1.get_width()/2), SCREEN_HEIGHT/8))
        screen.blit(line_2, (SCREEN_WIDTH/2 - (line_2.get_width()/2), SCREEN_HEIGHT*(3/8)))
        screen.blit(line_3, (SCREEN_WIDTH/2 - (line_3.get_width()/2), SCREEN_HEIGHT/2))

        screen.blit(player_1_text, (SCREEN_WIDTH*(2/3) - (player_1_text.get_width()/2), SCREEN_HEIGHT*(5/8)))
        screen.blit(player_2_text, (SCREEN_WIDTH/3 - (player_2_text.get_width()/2), SCREEN_HEIGHT*(5/8)))

        pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
        clock.tick(int(FRAME_RATE/4))  # Pause the clock to always maintain FRAME_RATE frames per second


def easy(ball_y, player_2):
    if ball_y < player_2.rect.center[1] and player_2.rect.top > 0:
        player_2.move(-1)
    elif ball_y > player_2.rect.center[1] and player_2.rect.bottom < SCREEN_HEIGHT:
        player_2.move(1)


def impossible(ball):
    temp_ball = Ball(SCREEN_HEIGHT, SCREEN_WIDTH)
    temp_ball.rect.center = ball.rect.center
    temp_ball.x_speed = ball.x_speed
    temp_ball.y_speed = ball.y_speed
    while temp_ball.rect.x > (SCREEN_WIDTH*(7/200)):
        temp_ball.update()
    final_y = temp_ball.rect.center[1] + (random.choice((1,0,-1)) * SCREEN_HEIGHT/24)
    del temp_ball
    return final_y


intro_menu()
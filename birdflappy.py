import random
import sys
import pygame
from pygame.locals import *
import os


# Global variable for the game
FPS = 32 # Frame per seconds
SCREENWIDTH = 289
SCREENHEIGHT = 511

# Getting a display screen 
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.85
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = r"assets/images/bird.png"
BACKGROUND = r"assets/images/bg.png"
PIPE = r"assets/images/pipe.png"

def welcomeScreen():
    playerx = int(SCREENWIDTH/10)
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height())/2.1)
    messagex = int((SCREENWIDTH - GAME_SPRITES["message"].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.01)
    basex = 0
    while True:

        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            # if event.type == QUIT or (event.key == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            
            #if user prsesses the sapce key or up key, start the game for them
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    return 
            
            #else display(blit) the images on screen
            else:
                screen.blit(GAME_SPRITES["background"], (0,0))
                screen.blit(GAME_SPRITES["player"], (playerx, playery))
                screen.blit(GAME_SPRITES["message"], (messagex, messagey))
                screen.blit(GAME_SPRITES["base"], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/10)
    playery = int(SCREENHEIGHT/2.1)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my list of upper pipe
    upperpipes = [
        {"x": SCREENWIDTH + 200, "y": newPipe1[0]["y"]},
        {"x": SCREENWIDTH +(SCREENWIDTH/2) , "y": newPipe2[0]["y"]}
    ]

    #my list of upper pipe
    lowerpipes = [
        {"x": SCREENWIDTH + 200, "y": newPipe1[1]["y"]},
        {"x": SCREENWIDTH +200+(SCREENWIDTH/2), "y": newPipe2[1]["y"]}
    ]
    
    # pipe's velocity in x direction
    pipeVelx = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerflapAccv = -8 # velocity while flapping
    playerflapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT :
            # if event.type == QUIT or (event.key == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if playery > 0:
                        playerVelY = playerflapAccv
                        playerflapped = True
                        GAME_SOUNDS["wing"].play()


        #crashtest will return true if player is crashed
        crashtest = isCollide(playerx, playery, upperpipes, lowerpipes)
        if crashtest:
            return 
        
        #check for score
        playerMidPos = playerx + GAME_SPRITES["player"].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe["x"] + GAME_SPRITES["pipe"][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS["point"].play()

        if playerVelY < playerMaxVelY and not playerflapped:
            playerVelY += playerAccY
        if playerflapped:
            playerflapped = False

        playerHeight = GAME_SPRITES["player"].get_height()
        playery += min(playerVelY, GROUNDY - playery - playerHeight )
        
        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperpipes, lowerpipes):
            upperPipe["x"] += pipeVelx
            lowerPipe["x"] += pipeVelx

        # add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperpipes[0]["x"] < 5:
            newpipe = getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
        if 0 < upperpipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        
        # if the pipe is out of the screen, remove it
        if upperpipes[0]["x"] < -GAME_SPRITES["pipe"][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # let's blit our sprites now
        screen.blit(GAME_SPRITES["background"], (0, 0))
        for upperPipe, lowerPipe in zip(upperpipes, lowerpipes):
            screen.blit(GAME_SPRITES["pipe"][0], (upperPipe["x"], upperPipe["y"])) 
            screen.blit(GAME_SPRITES["pipe"][1], (lowerPipe["x"], lowerPipe["y"])) 

        screen.blit(GAME_SPRITES["base"], (basex, GROUNDY))
        screen.blit(GAME_SPRITES["player"], (playerx, playery))

        mydigits = [int(x) for x in list(str(score))]
        width = 0

        for digit in mydigits:
            width += GAME_SPRITES["numbers"][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            screen.blit(GAME_SPRITES["numbers"][digit], (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES["numbers"][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS["swoosh"].play()
        return True

    for pipe in upperpipes:
        pipeheight = GAME_SPRITES["pipe"][0].get_height()
        if (playery < pipeheight + pipe["y"]) and abs(playerx - pipe["x"]) <= GAME_SPRITES["pipe"][0].get_width():
            GAME_SOUNDS["swoosh"].play()
            return True
        
    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            # GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe():
    pipeheight = GAME_SPRITES["pipe"][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - (GAME_SPRITES["base"].get_height()) - (1.2 * offset)))
    pipex = SCREENWIDTH +10
    y1 = pipeheight - y2 + offset
    pipe = [                   
        {"x": pipex, "y": -y1}, #upper pipe
        {"x": pipex, "y": y2}   #lower pipe
    ]
    return pipe 
    
                
if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Radhika")
    # path = r"C:\Users\Deepak\OneDrive\Desktop\Python\FlappyBirdGame\gallery\sprites\0.png"
    GAME_SPRITES['numbers'] = (
        pygame.image.load(r"assets/images/0.png").convert_alpha(),
        pygame.image.load(r"assets/images/1.png").convert_alpha(),
        pygame.image.load(r"assets/images/2.png").convert_alpha(),
        pygame.image.load(r"assets/images/3.png").convert_alpha(),
        pygame.image.load(r"assets/images/4.png").convert_alpha(),
        pygame.image.load(r"assets/images/5.png").convert_alpha(),
        pygame.image.load(r"assets/images/6.png").convert_alpha(),
        pygame.image.load(r"assets/images/7.png").convert_alpha(),
        pygame.image.load(r"assets/images/8.png").convert_alpha(),
        pygame.image.load(r"assets/images/9.png").convert_alpha()
    )

    GAME_SPRITES['message'] = pygame.image.load(r"assets/images/message.png").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(r"assets/images/base.png").convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(r"assets/images/bg.png").convert()
    GAME_SPRITES['player'] = pygame.image.load(r"assets/images/bird.png").convert()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(r"assets/images/pipe1.png").convert_alpha(), 180),
        pygame.image.load(r"assets/images/pipe1.png").convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound(r"assets/sounds/die.mp3")
    GAME_SOUNDS['wing'] = pygame.mixer.Sound(r"assets/sounds/wing.mp3")
    GAME_SOUNDS['point'] = pygame.mixer.Sound(r"assets/sounds/point.mp3")
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(r"assets/sounds/swoosh.mp3")
    # GAME_SOUNDS['die'] = pygame.mixer.Sound()
    # GAME_SOUNDS['die'] = pygame.mixer.Sound()
    # GAME_SOUNDS['die'] = pygame.mixer.Sound()
    # GAME_SOUNDS['die'] = pygame.mixer.Sound()

    while True:
        welcomeScreen() # Shows welcome screen to the user until the user presses the exit button
        mainGame() # This is the main game func
        

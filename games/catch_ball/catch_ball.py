import pygame
import sys
import cv2
from cvzone.HandTrackingModule import HandDetector
import random
from pygame import mixer

def start_ball():
    width = 1366
    height = 768

    # opencv code
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    # Hand Detector
    detector = HandDetector(maxHands=1, detectionCon=0.8)

    # Initialize the pygame
    pygame.init()

    # background sounds
    mixer.music.load('games/catch_ball/music/background.mp3')
    mixer.music.play(loops=-1)

    closedHand_sound = mixer.Sound('games/catch_ball/music/slap.wav')
    catching_sound = mixer.Sound('games/catch_ball/music/catching_sound.wav')

    # Define the screen
    screen = pygame.display.set_mode((width, height))

    # Timer
    clock = pygame.time.Clock()
    currentTime = 1
    game_over = False  # Flag to track game over
    score_stopped = False  # Flag to track if score incrementation should stop

    # Title and Icon
    pygame.display.set_caption("Catch Ball")
    icon = pygame.image.load('games/catch_ball/images/ball_32.png').convert_alpha()
    pygame.display.set_icon(icon)
    backgroundImg = pygame.image.load('games/catch_ball/images/TennisBack.png').convert()

    # Player
    playerPosition = [370, 480]
    playerMovement = [0, 0]
    x = width/2 - 64
    y = height/2 - 64
    openHandImg = pygame.image.load('games/catch_ball/images/openHand.png').convert_alpha()
    openHandImg = pygame.transform.scale(openHandImg, (128, 128))
    openHand_rect = openHandImg.get_rect(topleft=(x, y))

    closedHandImg = pygame.image.load('games/catch_ball/images/closedHand.png').convert_alpha()
    closedHandImg = pygame.transform.scale(closedHandImg, (128, 128))
    closedHand_rect = closedHandImg.get_rect(topleft=(x, y))

    # Insects
    InsectImg = []
    InsectX = []
    InsectY = []
    insect_rect = []
    insectMoveX = []
    insectMoveY = []
    numberOfInsects = 10
    for i in range(numberOfInsects):
        InsectX.append(random.randint(0, 1366))
        InsectY.append(random.randint(0, 768))
        InsectImg.append(pygame.image.load('games/catch_ball/images/ball_32.png').convert_alpha())
        insect_rect.append(InsectImg[i].get_rect(topleft=(InsectX[i], InsectY[i])))
        insectMoveX.append(10)
        insectMoveY.append(8)

    ## Game Texts
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    gameOver_font = pygame.font.Font('freesansbold.ttf', 100)
    textX = 10
    textY = 10
    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def show_timer():
        nonlocal game_over, score_stopped  # Access the game_over and score_stopped flags from the enclosing scope
        if currentTime / 1000 >= 60:  # Change 100 to 60 for 60 seconds timer
            timer = font.render("Time: " + str(int(61 - currentTime / 1000)), True, (255, 0, 0))
        else:
            timer = font.render("Time: " + str(int(61 - currentTime / 1000)), True, (255, 255, 255))  # Adjust text color as needed
        screen.blit(timer, (1210, 10))
        if currentTime / 1000 >= 61:  # Adjust the end time accordingly
            game_over = True  # Set the game over flag
            gameOver = gameOver_font.render("Game Over!", True, (255, 0, 0))
            screen.blit(gameOver, (width / 2 - 300, height / 2 - 30))
        elif currentTime / 1000 >= 60 and not score_stopped:  # Stop score incrementation if timer is zero
            score_stopped = True

    indexes_for_closed_fingers = [8, 12, 16, 20]
    catch_insect_with_openHand = False
    fingers = [0, 0, 0, 0]
    while not game_over:
        screen.blit(backgroundImg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        success, frame = cap.read()
        hands, frame = detector.findHands(frame)

        if hands:
            lmList = hands[0]
            positionOfTheHand = lmList['lmList']
            openHand_rect.left = (positionOfTheHand[9][0] - 200) * 1.5
            openHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5
            closedHand_rect.left = (positionOfTheHand[9][0] - 200) * 1.5
            closedHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5

            hand_is_closed = 0
            for index in range(0, 4):
                if positionOfTheHand[indexes_for_closed_fingers[index]][1] > positionOfTheHand[indexes_for_closed_fingers[index] - 2][1]:
                    fingers[index] = 1
                else:
                    fingers[index] = 0
                if fingers[0]*fingers[1]*fingers[2]*fingers[3]:
                    if hand_is_closed and catch_insect_with_openHand == False:
                        closedHand_sound.play()
                    hand_is_closed = 0
                    screen.blit(closedHandImg, closedHand_rect)
                    for iteration in range(numberOfInsects):
                        if openHand_rect.colliderect(insect_rect[iteration]) and catch_insect_with_openHand:
                            if not score_stopped:  # Check if score incrementation is allowed
                                score_value += 1
                                catching_sound.play()
                                catch_insect_with_openHand = False
                                insect_rect[iteration] = InsectImg[iteration].get_rect(topleft=(random.randint(0, 1366), random.randint(0, 768)))
                    catch_insect_with_openHand = False
                else:
                    screen.blit(openHandImg, openHand_rect)
                    hand_is_closed = 1
                    for iterate in range(numberOfInsects):
                        if openHand_rect.colliderect(insect_rect[iterate]):
                            catch_insect_with_openHand = True

        cv2.imshow("webcam", frame)

        for i in range(numberOfInsects):
            insect_rect[i].right += insectMoveX[i]
            if insect_rect[i].right <= 16:
                insectMoveX[i] += 10
            elif insect_rect[i].right >= width:
                insectMoveX[i] -= 10

            insect_rect[i].top += insectMoveY[i]
            if insect_rect[i].top <= 0:
                insectMoveY[i] += 8
            elif insect_rect[i].top >= height-32:
                insectMoveY[i] -= 8
            screen.blit(InsectImg[i], insect_rect[i])

        show_score(textX, textY)
        currentTime = pygame.time.get_ticks()
        show_timer()

        pygame.display.update()
        clock.tick(60)

    # Game over logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    start_ball()

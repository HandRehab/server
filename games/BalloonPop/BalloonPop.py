# Import
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time


def start_balloon(q):
    # print(name)
    # Initialize
    pygame.init()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Balloon Pop")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # width
    cap.set(4, 720)  # height

    # Images
    imgBalloon = pygame.image.load('games/BalloonPop/Resources/BalloonRed.png').convert_alpha()
    rectBalloon = imgBalloon.get_rect()
    rectBalloon.x, rectBalloon.y = 500, 300

    # Variables
    speed = 15
    score = 0
    startTime = time.time()
    totalTime = 60

    # Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)


    def resetBalloon():
        rectBalloon.x = random.randint(100, img.shape[1] - 100)
        rectBalloon.y = img.shape[0] + 50


    # Main loop
    game_running = True
    game_over = False

    try:
        while game_running:
            # Get Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    # pygame.quit()
                    # print('Closed abruptly')
                    # return "Closed abruptly"

            # Apply Logic
            timeRemain = int(totalTime -(time.time()-startTime))
            if timeRemain < 0:
                game_over = True

            if game_over:
                window.fill((255,255,255))

                font = pygame.font.Font('games/BalloonPop/Resources/Marcellus-Regular.ttf', 50)
                textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
                textTime = font.render(f'Time UP', True, (50, 50, 255))
                window.blit(textScore, (450, 350))
                window.blit(textTime, (530, 275))
                pygame.display.update()
                continue

                # for event in pygame.event.get():
                #     if event.type == pygame.QUIT:
                #         game_running = False
                #         pygame.quit()
                #         print("game over")
                #         return {"score": textScore, "name": name}

                    

            else:
                # OpenCV
                success, img = cap.read()
                img = cv2.flip(img, 1)
                hands, img = detector.findHands(img, flipType=False)

                rectBalloon.y -= speed  # Move the balloon up
                # check if balloon has reached the top without pop
                if rectBalloon.y < 0:
                    resetBalloon()
                    speed += 1

                if hands:
                    hand = hands[0]
                    x, y = hand['lmList'][8][0:2]
                    if rectBalloon.collidepoint(x, y):
                        resetBalloon()
                        score += 1
                        

                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                imgRGB = np.rot90(imgRGB)
                frame = pygame.surfarray.make_surface(imgRGB).convert()
                frame = pygame.transform.flip(frame, True, False)
                window.blit(frame, (0, 0))
                window.blit(imgBalloon, rectBalloon)

                font = pygame.font.Font('games/BalloonPop/Resources/Marcellus-Regular.ttf', 50)
                textScore = font.render(f'Score: {score}', True, (50, 50, 255))
                textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
                window.blit(textScore, (35, 35))
                window.blit(textTime, (1000, 35))

            # Update Display
            pygame.display.update()
            # Set FPS
            clock.tick(fps)

    except Exception as e:
        print(f"Error occurred: {e}")
        q.put({"status": "An error occured"})  # If an error occurs, return an error message

    finally:
        pygame.quit()
        cap.release()  # Release the webcam
        cv2.destroyAllWindows()  # Close all OpenCV windows

    if game_over:
        q.put({"score": score, "status": "Game over"})
    
    else:
        q.put({"status": "Closed abruptly"})
   
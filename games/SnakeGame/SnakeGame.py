import math
import random
import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

async def start_snake():
    print("game started")
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8, maxHands=1)

    class SnakeGameClass:
        def __init__(self, pathFood):
            print("Hellooooo")
            self.points = []  # all points of the snake
            self.lengths = []  # distance between each point
            self.currentLength = 0  # total length of the snake
            self.allowedLength = 150  # total allowed Length
            self.previousHead = 0, 0  # previous head point

            self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
            if self.imgFood is None:
                raise FileNotFoundError(f"Unable to load image from path: {pathFood}")

            self.hFood, self.wFood, _ = self.imgFood.shape
            self.foodPoint = 0, 0
            self.randomFoodLocation()

            self.score = 0
            self.gameOver = True  # Start the game as over

        def randomFoodLocation(self):
            self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

        def update(self, imgMain, currentHead):
            if self.gameOver:
                cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                                   scale=7, thickness=5, offset=20)
                cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],
                                   scale=7, thickness=5, offset=20)
            else:
                px, py = self.previousHead
                cx, cy = currentHead

                self.points.append([cx, cy])
                distance = math.hypot(cx - px, cy - py)
                self.lengths.append(distance)
                self.currentLength += distance
                self.previousHead = cx, cy

                # Length Reduction
                if self.currentLength > self.allowedLength:
                    for i, length in enumerate(self.lengths):
                        self.currentLength -= length
                        self.lengths.pop(i)
                        self.points.pop(i)
                        if self.currentLength < self.allowedLength:
                            break

                # Check if snake ate the Food
                rx, ry = self.foodPoint
                if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                        ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                    self.randomFoodLocation()
                    self.allowedLength += 50
                    self.score += 1
                    print(self.score)

                # Draw Snake
                if self.points:
                    for i, point in enumerate(self.points):
                        if i != 0:
                            cv2.line(imgMain, tuple(self.points[i - 1]), tuple(self.points[i]), (0, 0, 255), 20)
                    cv2.circle(imgMain, tuple(self.points[-1]), 20, (0, 255, 0), cv2.FILLED)

                # Draw Food
                imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                            (rx - self.wFood // 2, ry - self.hFood // 2))

                cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                                   scale=3, thickness=3, offset=10)

                # Check for Collision
                if len(self.points) > 2:
                    pts = np.array(self.points[:-2], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
                    minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

                    if -1 <= minDist <= 1:
                        print("Hit")
                        self.gameOver = True
                        self.points = []  # all points of the snake
                        self.lengths = []  # distance between each point
                        self.currentLength = 0  # total length of the snake
                        self.allowedLength = 150  # total allowed Length
                        self.previousHead = 0, 0  # previous head point
                        self.randomFoodLocation()

            return imgMain

        def get_score(self):
            return self.score

    game = SnakeGameClass("games/SnakeGame/donut.png")
    game.gameOver = False  # Set game as active initially

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        if hands:
            lmList = hands[0]['lmList']
            pointIndex = lmList[8][0:2]
            game.gameOver = False  # Set game as active when hand is detected
            img = game.update(img, pointIndex)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    score = game.get_score()
    print(score)
    cap.release()
    cv2.destroyAllWindows()


    return score




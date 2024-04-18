import mediapipe as mp
import cv2
import math
import time


async def box_play():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    color = (0, 0, 255)

    # Score variable
    score = 0

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands()

    succ_top_left = (1300,700)
    succ_bottom_right= (1500,500)

    success_top_left = (800, 800)
    success_bottom_right = (1500, 500)

    # Bounding box for the hand
    top_left = (20, 480)
    bottom_right = (220, 680)

    # Barrier rectangle coordinates
    barrier_top_left = (700, 1000)
    barrier_bottom_right = (780, 400)

    # Initial position for the bounding box
    initial_top_left = top_left
    initial_bottom_right = bottom_right

    # Timer setup
    start_time = time.time()
    duration = 60  # Set the duration of the timer in secondsq

    def calculate_distance(x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = cv2.flip(imgRGB, 1)
        results = hands.process(imgRGB)

        img = cv2.resize(img, (0, 0), fx=2, fy=1.5)
        img = cv2.flip(img, 1)

        # Draw the barrier rectangle
        cv2.rectangle(img, barrier_top_left, barrier_bottom_right, (255, 0,0 ), cv2.FILLED)

        # Draw the success rectangle
        #cv2.rectangle(img, success_top_left, success_bottom_right, (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, succ_top_left, succ_bottom_right, (0, 0, 255), thickness= 2)

        # Calculate the remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(0, duration - elapsed_time)
        remaining_time_str = f"Time: {int(remaining_time)}s"

        # Display the remaining time and score at the top-left corner
        display_text = f"Score: {score} | {remaining_time_str}"
        cv2.putText(img, display_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if results.multi_hand_landmarks:
            for handLM in results.multi_hand_landmarks:
                index_finger = None
                thumb_finger = None
                middle_finger = None
                for id, lm in enumerate(handLM.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    if id == 4:
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        cv2.circle(center=(cx, cy), img=img, color=(0, 0, 255), radius=15, thickness=-1)
                        thumb_finger = (cx, cy)
                    if id == 8:
                        cv2.circle(center=(cx, cy), img=img, color=(0, 0, 255), radius=20, thickness=-1)
                        index_finger = (cx, cy)
                    if id == 12:
                        cv2.circle(center=(cx, cy), img=img, color=(0, 0, 255), radius=20, thickness=-1)
                        middle_finger = (cx, cy)
                    if index_finger and thumb_finger:
                        res = calculate_distance(index_finger[0], index_finger[1], thumb_finger[0], thumb_finger[1])
                        if top_left[0] < index_finger[0] < bottom_right[0] and top_left[1] < index_finger[1] < bottom_right[1]:
                            if res < 50:
                                top_left = (index_finger[0] - 100, index_finger[1] - 100)
                                bottom_right = (index_finger[0] + 100, index_finger[1] + 100)

                
                    if (
                        barrier_top_left[0] > top_left[0] and barrier_top_left[0] < bottom_right[0]
                        and barrier_top_left[1] > top_left[1] and barrier_top_left[1] < bottom_right[1]
                        ) or (
                        barrier_bottom_right[0] > top_left[0] and barrier_bottom_right[0] < bottom_right[0]
                        and barrier_bottom_right[1] > top_left[1] and barrier_bottom_right[1] < bottom_right[1]
                        ) or (
                        top_left[0] < barrier_top_left[0] and bottom_right[0] > barrier_bottom_right[0]
                        and top_left[1] < barrier_top_left[1] and bottom_right[1] > barrier_bottom_right[1]
                        ):
            # Reset to the initial position
                        top_left = initial_top_left
                        bottom_right = initial_bottom_right
                        if score!= 0:
                            score-=1
                    
                    if (
                        (top_left[0] < success_top_left[0] < bottom_right[0] or top_left[0] < success_bottom_right[0] < bottom_right[0])
                        and (top_left[1] < success_top_left[1] < bottom_right[1] or top_left[1] < success_bottom_right[1] < bottom_right[1])):
                        top_left = initial_top_left
                        bottom_right = initial_bottom_right
                        score+=1
                        
                mp_draw.draw_landmarks(img, handLM, mp_hands.HAND_CONNECTIONS)

        # Check for intersection with the barrier rectangle
        

        # Draw the hand bounding box
        cv2.rectangle(img, top_left, bottom_right, color, cv2.FILLED)

        cv2.imshow("frame", img)
        if cv2.waitKey(1) & 0xFF == ord('q') or elapsed_time >= duration:
            break

    cap.release()
    cv2.destroyAllWindows()
    

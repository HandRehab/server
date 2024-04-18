import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
GAME_DURATION = 60  # 60 seconds

class HandTracking:
    def __init__(self):
        self.hand_tracking = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.hand_x = 0
        self.hand_y = 0
        self.results = None
        self.score = 0
        self.prev_hand_closed = False

    def scan_hands(self, image):
        rows, cols, _ = image.shape

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        self.results = self.hand_tracking.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        hand_closed = False

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y

                self.hand_x = int(x * SCREEN_WIDTH)
                self.hand_y = int(y * SCREEN_HEIGHT)

                x1, y1 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y

                if y1 > y and not self.prev_hand_closed:
                    hand_closed = True
                    self.score += 1
                    self.prev_hand_closed = True
                elif y1 < y:
                    self.prev_hand_closed = False

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        return image, hand_closed

    def get_hand_center(self):
        return (self.hand_x, self.hand_y)

    def get_score(self):
        return self.score

def start_punch():
    # Initialize HandTracking object
    hand_tracker = HandTracking()

    # Open camera
    cap = cv2.VideoCapture(0)

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Scan hands
        frame_with_hands, hand_closed = hand_tracker.scan_hands(frame)

        # Get hand center
        hand_center = hand_tracker.get_hand_center()
        # Get score
        score = hand_tracker.get_score()

        # Display score
        cv2.putText(frame_with_hands, f"Score: {score}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Display timer
        cv2.putText(frame_with_hands, f"Time left: {int(GAME_DURATION - elapsed_time)}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Tracking", frame_with_hands)

        # End the game if time limit is reached
        if elapsed_time >= GAME_DURATION:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage:
start_punch()

import cv2
import mediapipe as mp
import math

class HandDetector:
    """
    Detects hands using MediaPipe and extracts landmarks.
    """
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        """
        Initialize the MediaPipe Hands model.
        :param mode: Static image mode (False for video stream).
        :param max_hands: Maximum number of hands to detect.
        :param detection_con: Minimum detection confidence.
        :param track_con: Minimum tracking confidence.
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """
        Processes the image to find hands and optionally draws landmarks.
        :param img: Image to process (BGR).
        :param draw: Whether to draw landmarks on the image.
        :return: Processed image.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        """
        Extracts landmark positions from the detected hand.
        :param img: Image to process.
        :param hand_no: Index of the hand to process (default 0).
        :param draw: Whether to draw specific landmarks (optional).
        :return: List of landmarks [id, x, y].
        """
        lm_list = []
        if self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                my_hand = self.results.multi_hand_landmarks[hand_no]
                h, w, c = img.shape
                for id, lm in enumerate(my_hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                    if draw:
                        # Draw a circle on the wrist or other key points if needed
                        pass
        return lm_list

    def get_bbox(self, img, lm_list, draw=True):
        """
        Get the bounding box of the hand.
        """
        if not lm_list:
            return None
        
        x_list = [lm[1] for lm in lm_list]
        y_list = [lm[2] for lm in lm_list]
        xmin, xmax = min(x_list), max(x_list)
        ymin, ymax = min(y_list), max(y_list)
        
        if draw:
            cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
            
        return (xmin, ymin, xmax, ymax)

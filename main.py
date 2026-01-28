import cv2
import time
import numpy as np
from hand_detector import HandDetector
from gesture_classifier import GestureClassifier
from keyboard_controller import KeyboardController

def main():
    # 1. Initialization
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) # Width
    cap.set(4, 480) # Height

    detector = HandDetector(max_hands=1, detection_con=0.7, track_con=0.5)
    classifier = GestureClassifier()
    controller = KeyboardController()

    # Stability / Debounce variables
    current_stable_gesture = "IDLE"
    pending_gesture = "IDLE"
    pending_start_time = 0
    STABILITY_DELAY = 0.150 # 150ms

    pTime = 0

    print("Starting Hand Gesture Controller...")
    print("Press 'q' to exit.")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from webcam.")
            break

        # Flip image for mirror view
        img = cv2.flip(img, 1)

        # 2. Find Hands
        img = detector.find_hands(img)
        lm_list = detector.find_position(img, draw=False)

        # 3. Classify Gesture
        detected_gesture = "IDLE"
        if len(lm_list) != 0:
            # Check which hand (Left or Right)
            # MediaPipe's "Right" is "Left" in mirror mode if not handled?
            # Actually, standard MediaPipe output: 
            # If I show my Right hand to camera, it looks like Left hand on screen (mirror).
            # But the label 'Right' usually corresponds to the user's Right hand if we don't flip input BEFORE processing?
            # detector.find_hands takes RGB.
            # Let's check handedness if needed, but for now assuming Right Hand User controls.
            # Or we can just pass the first hand's label.
            
            # Simple handedness check (not fully robust in wrapper but sufficient for single hand)
            # For this classifier, we tell it "Right" or "Left" based on the wrist vs pinky?
            # Let's trust the classifier's internal logic or pass a default if unsure.
            # Our classifier uses simple "Right" logic by default.
            
            detected_gesture = classifier.classify(lm_list, hand_label="Right") 

        # 4. Stability Logic
        if detected_gesture != current_stable_gesture:
            if detected_gesture == pending_gesture:
                if (time.time() - pending_start_time) > STABILITY_DELAY:
                    current_stable_gesture = detected_gesture
                    # Execute Action
                    if current_stable_gesture == "GAS":
                        controller.press_gas()
                    elif current_stable_gesture == "BRAKE":
                        controller.press_brake()
                    else:
                        controller.release_all()
            else:
                pending_gesture = detected_gesture
                pending_start_time = time.time()
        else:
            pending_gesture = None

        # 5. Visual Feedback
        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        # Gesture Status
        status_color = (255, 0, 0) # Blue for IDLE
        if current_stable_gesture == "GAS":
            status_color = (0, 255, 0) # Green
        elif current_stable_gesture == "BRAKE":
            status_color = (0, 0, 255) # Red

        cv2.rectangle(img, (0, 400), (640, 480), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f'GESTURE: {current_stable_gesture}', (20, 450), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, status_color, 3)

        # Show Pending if evaluating
        if pending_gesture and pending_gesture != current_stable_gesture:
             cv2.putText(img, '.', (580, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

        cv2.imshow("Hand Gesture Controller", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    controller.release_all()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

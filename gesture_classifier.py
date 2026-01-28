import math

class GestureClassifier:
    """
    Classifies hand gestures based on landmark positions.
    """
    def __init__(self, retention_duration=5):
        """
        :param retention_duration: Number of frames to hold a state for stability (not fully used in this simple logic, 
                                   but good for future expansion). 
                                   For latency reasons, we might prefer direct classification with a buffer in main loop.
        """
        self.tip_ids = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky
        
    def classify(self, lm_list, hand_label="Right"):
        """
        Determines the gesture based on finger states.
        :param lm_list: List of landmarks [id, x, y].
        :param hand_label: "Right" or "Left" (from MediaPipe).
        :return: Gesture String ("GAS", "BRAKE", "IDLE", "UNKNOWN")
        """
        if not lm_list:
            return "IDLE"

        fingers = []

        # Thumb
        # Logic: Compare Thumb Tip (4) x with Thumb IP (3) x
        # If Right Hand: Thumb is on left side. Extended means Tip.x < IP.x
        # If Left Hand: Thumb is on right side. Extended means Tip.x > IP.x
        # Note: This assumes palm facing camera.
        if hand_label == "Right":
            if lm_list[self.tip_ids[0]][1] < lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1) # Open
            else:
                fingers.append(0) # Closed
        else:
            if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1) # Open
            else:
                fingers.append(0) # Closed

        # 4 Fingers (Index, Middle, Ring, Pinky)
        # Logic: Tip.y < Pip.y (Tip is above Joint) => Open
        # y increases downwards in OpenCV
        for id in range(1, 5):
            if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # gestures
        # GAS: Index (1) extended, others (0, 2, 3, 4) folded -> [0, 1, 0, 0, 0]
        # BRAKE: All folded -> [0, 0, 0, 0, 0]
        # IDLE: Open Palm -> [1, 1, 1, 1, 1] or mostly open
        
        # Strict mapping as per requirements
        
        if fingers == [0, 1, 0, 0, 0] or fingers == [1, 1, 0, 0, 0]: 
            # Allow Thumb open or closed for GAS? Requirement says "thumb + middle + ring + pinky folded".
            # So strictly [0, 1, 0, 0, 0]. 
            # But sometimes thumb detection is jittery. Let's aim for strict first.
            if fingers == [0, 1, 0, 0, 0]:
                return "GAS"
        
        if fingers == [0, 0, 0, 0, 0]:
            return "BRAKE"
        
        if fingers == [1, 1, 1, 1, 1]:
            return "IDLE"
            
        # Optional: Relaxed IDLE (e.g. if 4 fingers up)
        # But requirement says "Determine finger states... Classify gestures".
        # We will return IDLE for anything else to be safe (release keys).
        return "IDLE"

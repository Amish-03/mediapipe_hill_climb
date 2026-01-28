from pynput.keyboard import Key, Controller
import time

class KeyboardController:
    """
    Controls keyboard input (Left/Right arrows) based on commands.
    """
    def __init__(self):
        self.keyboard = Controller()
        self.current_action = None # 'GAS', 'BRAKE', 'IDLE'

    def press_gas(self):
        """
        Presses RIGHT arrow (GAS) and releases LEFT arrow (BRAKE).
        """
        if self.current_action != 'GAS':
            self.keyboard.release(Key.left)
            self.keyboard.press(Key.right)
            self.current_action = 'GAS'
            # print("Action: GAS (Right Arrow)")

    def press_brake(self):
        """
        Presses LEFT arrow (BRAKE) and releases RIGHT arrow (GAS).
        """
        if self.current_action != 'BRAKE':
            self.keyboard.release(Key.right)
            self.keyboard.press(Key.left)
            self.current_action = 'BRAKE'
            # print("Action: BRAKE (Left Arrow)")

    def release_all(self):
        """
        Releases both keys.
        """
        if self.current_action != 'IDLE':
            self.keyboard.release(Key.right)
            self.keyboard.release(Key.left)
            self.current_action = 'IDLE'
            # print("Action: IDLE (Released All)")

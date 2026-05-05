

class ButtonManager:
    def __init__(self, base):
        self.btn0 = base.buttons[0]
        self.btn1 = base.buttons[1]
        self.btn2 = base.buttons[2]
        self.btn3 = base.buttons[3]
        self._prev = {f'btn{i}': False for i in range(4)}

    def read_buttons(self) -> dict[str, bool]:
        return {
            'btn0': self.btn0.read(),
            'btn1': self.btn1.read(),
            'btn2': self.btn2.read(),
            'btn3': self.btn3.read()
        }

    def read_pressed(self) -> dict[str, bool]:
        """Returns buttons that transitioned low→high since last call."""
        cur = self.read_buttons()
        pressed = {k: cur[k] and not self._prev[k] for k in cur}
        self._prev = cur
        return pressed


# Keys: 1→btn0, 2→btn1, 3→btn2, 4→btn3
_KEY_MAP = {ord('1'): 'btn0', ord('2'): 'btn1', ord('3'): 'btn2', ord('4'): 'btn3'}

class LocalButtonManager:
    def __init__(self):
        self._state = {f'btn{i}': False for i in range(4)}
        self._prev  = {f'btn{i}': False for i in range(4)}

    def update(self, key: int):
        """Call each frame with the result of cv2.waitKey()."""
        self._prev = dict(self._state)
        for k in self._state:
            self._state[k] = False
        if key in _KEY_MAP:
            self._state[_KEY_MAP[key]] = True

    def read_buttons(self) -> dict[str, bool]:
        return dict(self._state)

    def read_pressed(self) -> dict[str, bool]:
        """Returns buttons that transitioned low→high this frame."""
        return {k: self._state[k] and not self._prev[k] for k in self._state}


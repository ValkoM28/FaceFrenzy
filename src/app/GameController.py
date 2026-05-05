import random
from enum import Enum, auto


class GameState(Enum):
    SETUP = auto()
    IDLE = auto()
    COUNTDOWN = auto()
    CAPTURE = auto()
    RESULT = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class GameController:
    def __init__(
        self,
        face_count_min=1,
        face_count_max=6,
        base_countdown=10.0,
        result_display_duration=2.5,
        max_lives=3,
        countdown_formula=None,
    ):
        self._face_count_min = face_count_min
        self._face_count_max = face_count_max
        self._in_setup = True

    # --- setup ---

    @property
    def face_count_max(self) -> int:
        return self._face_count_max

    def inc_max_faces(self):
        self._face_count_max += 1

    def dec_max_faces(self):
        if self._face_count_max > 2:
            self._face_count_max -= 1

    def confirm_setup(self):
        self._in_setup = False
        self.start_game()

    # --- actions ---

    def start_game(self):
        pass

    def update(self, dt: float):
        pass

    def submit_face_count(self, count: int):
        pass

    def toggle_pause(self):
        pass

    def reset(self):
        pass

    # --- read-only properties ---

    @property
    def state(self) -> GameState:
        if self._in_setup:
            return GameState.SETUP
        return None  # remaining states are stubs

    @property
    def lives(self) -> int:
        pass

    @property
    def score(self) -> int:
        pass

    @property
    def round_number(self) -> int:
        pass

    @property
    def target_count(self) -> int:
        pass

    @property
    def countdown_remaining(self) -> float:
        pass

    @property
    def last_result(self):
        """Returns 'MATCH', 'MISS', or None."""
        pass

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
        self.face_count_min = face_count_min
        self.face_count_max = face_count_max
        self.state = GameState.SETUP
        self.score = 0
        self.lives = max_lives
        self.countdown_remaining = 10.0
        self.result_display_remaining = 0.0
        self.target_count = 0
        self.last_result = None  # 'MATCH', 'MISS', or None
        self.last_submitted_count = 0


    # --- setup ---

    # @property
    # def face_count_max(self) -> int:
    #     return self.face_count_max

    def inc_max_faces(self):
        self.face_count_max += 1

    def dec_max_faces(self):
        if self.face_count_max > 2:
            self.face_count_max -= 1

    def confirm_setup(self):
        self.state = GameState.IDLE
        self.score = 0
        self.lives = 3
        self.next_round()
    # --- actions ---
    def next_round(self):
        self.target_count = random.randint(self.face_count_min, self.face_count_max)
        self.countdown_remaining = 10.0
        self.state = GameState.COUNTDOWN

    # def start_game(self):
    #     pass 

    def update(self, dt: float):
        if self.state == GameState.COUNTDOWN:
            self.countdown_remaining -= dt
            # print(f"Countdown: {self.countdown_remaining:.2f}s remaining")
            if self.countdown_remaining <= 0:
                self.state = GameState.CAPTURE
                # self._evaluate_result()
        elif self.state == GameState.RESULT:
            self.result_display_remaining -= dt
            if self.result_display_remaining <= 0:
                if self.lives <= 0:
                    self.state = GameState.GAME_OVER
                else:
                    self.next_round()
        elif self.state == GameState.CAPTURE:
            self._evaluate_result()
            

    def submit_face_count(self, count: int):
        print(f"Submitted face count: {count}")
        self.last_submitted_count = count

    def toggle_pause(self):
        pass

    def reset(self):
        pass

    def _evaluate_result(self):

        if self.target_count == self.last_submitted_count:
            self.score += 1
            self.last_result = 'MATCH'
        else:
            self.last_result = 'MISS'
            self.lives -= 1
        self.result_display_remaining = 2.5
        self.state = GameState.RESULT

    # --- read-only properties ---

    # @property
    # def state(self) -> GameState:
    #     return self._state  # remaining states are stubs

    # @property
    # def lives(self) -> int:
    #     pass

    # @property
    # def score(self) -> int:
    #     pass

    # @property
    # def round_number(self) -> int:
    #     pass

    # @property
    # def target_count(self) -> int:
    #     pass

    # @property
    # def countdown_remaining(self) -> float:
    #     pass

    # @property
    # def last_result(self):
    #     """Returns 'MATCH', 'MISS', or None."""
    #     pass

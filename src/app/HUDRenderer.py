import cv2


FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 220, 0)
RED = (0, 0, 220)
YELLOW = (0, 220, 220)


class HUDRenderer:
    def __init__(self, frame_width, frame_height, font_scale=0.8, show_fps=False):
        self.w = frame_width
        self.h = frame_height
        self.font_scale = font_scale
        self.show_fps = show_fps

    def render(self, frame, controller):
        """Composite HUD onto frame based on controller state. Returns annotated frame."""
        out = frame.copy()

        state = controller.state
        if state is None:
            self._put_text(out, "STUB MODE — controller not implemented", (10, self.h // 2), WHITE)
            return out

        self._render_lives(out, controller.lives)
        self._render_score(out, controller.score)

        from GameController import GameState
        if state == GameState.IDLE:
            self._render_idle(out)
        elif state == GameState.COUNTDOWN:
            self._render_countdown(out, controller)
        elif state == GameState.RESULT:
            self._render_result(out, controller)
        elif state == GameState.GAME_OVER:
            self._render_game_over(out, controller)
        elif state == GameState.PAUSED:
            self._put_centered(out, "PAUSED", WHITE)

        return out

    def _render_idle(self, frame):
        self._put_centered(frame, "Press any key to start", WHITE)

    def _render_countdown(self, frame, controller):
        remaining = controller.countdown_remaining
        target = controller.target_count
        label = f"Faces: {target}   Time: {remaining:.1f}s" if remaining is not None else "Faces: ?"
        self._put_centered(frame, label, YELLOW)

    def _render_result(self, frame, controller):
        result = controller.last_result
        if result == "MATCH":
            self._put_centered(frame, "MATCH!", GREEN)
        elif result == "MISS":
            self._put_centered(frame, "MISS", RED)

    def _render_game_over(self, frame, controller):
        score = controller.score
        msg = f"GAME OVER  Score: {score}" if score is not None else "GAME OVER"
        self._put_centered(frame, msg, RED)
        self._put_centered(frame, "Press R to restart", WHITE, y_offset=40)

    def _render_lives(self, frame, lives):
        if lives is None:
            return
        hearts = "* " * lives
        self._put_text(frame, hearts, (10, 30), RED)

    def _render_score(self, frame, score):
        if score is None:
            return
        self._put_text(frame, f"Score: {score}", (self.w - 160, 30), WHITE)

    # --- helpers ---

    def _put_text(self, frame, text, pos, color, scale=None, thickness=2):
        s = scale or self.font_scale
        cv2.putText(frame, text, pos, FONT, s, BLACK, thickness + 2, cv2.LINE_AA)
        cv2.putText(frame, text, pos, FONT, s, color, thickness, cv2.LINE_AA)

    def _put_centered(self, frame, text, color, y_offset=0, scale=None):
        s = scale or self.font_scale
        (tw, _), _ = cv2.getTextSize(text, FONT, s, 2)
        x = (self.w - tw) // 2
        y = self.h // 2 + y_offset
        self._put_text(frame, text, (x, y), color, scale=s)

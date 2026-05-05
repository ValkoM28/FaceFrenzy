import cv2


class HUDRenderer:
    def __init__(self, frame_width, frame_height, font_scale=0.8, show_fps=False):
        pass

    def render(self, frame, controller):
        """Composite HUD onto frame based on controller state. Returns annotated frame."""
        pass

    def _render_idle(self, frame):
        pass

    def _render_countdown(self, frame, controller):
        pass

    def _render_result(self, frame, controller):
        pass

    def _render_game_over(self, frame, controller):
        pass

    def _render_lives(self, frame, lives):
        pass

    def _render_score(self, frame, score):
        pass

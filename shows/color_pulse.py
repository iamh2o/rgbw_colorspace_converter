from color import HSV
from grid import every, inset

from .showbase import ShowBase


class ColorPulse(ShowBase):
    """Simple color pulse from a base color where the saturation is gently adjusted up and down."""
    def __init__(self, pyramid, frame_delay=0.2):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

        # Knobs to change for effect
        self.hue = 351
        self.low_saturation = 0.8
        self.high_saturation = 1.0
        self.steps = 3

        # Not sure of the proper formula for this, but allows running on normal or mega triangle.
        self.max_distance = 0
        while self.grid.select(inset(self.max_distance)):
            self.max_distance += 1

        self.saturation_step = (self.high_saturation - self.low_saturation) / self.steps

    @staticmethod
    def description() -> str:
        return 'pulse where saturation gently fluctuates'

    def next_frame(self):
        color = HSV(self.hue/360, self.low_saturation, 1.0)

        while True:
            # 1. Paint the triangle the color
            self.grid.set(every, color)
            yield self.frame_delay

            # 2. From center outward, adjust the saturation up like a wave
            for distance in range(self.max_distance, -1, -1):
                self.saturate_from_distance(color, distance, self.saturation_step)
                yield self.frame_delay

            # 3. From center outward, adjust the saturation down like a wave
            for distance in range(self.max_distance, -1, -1):
                self.saturate_from_distance(color, distance, -self.saturation_step)
                yield self.frame_delay

    def saturate_from_distance(self, color, distance, saturation_delta):
        """Saturates color steps from a distance (from center) outward."""
        for step in range(0, self.steps + 1):
            for i in range(step + 1):
                saturation = self.low_saturation if saturation_delta > 0 else self.high_saturation
                saturation = saturation + (saturation_delta * (step - i))
                new_color = HSV(color.h, saturation, 1.0)

                if distance - i < 0:
                    continue
                self.grid.set(inset(distance - i), new_color)

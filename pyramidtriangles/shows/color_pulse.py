from ..color import HSV
from ..grid import every, inset
from . import Show, ValueKnob, HSVKnob


class ColorPulse(Show):
    """Simple color pulse from a base color where the saturation is gently adjusted up and down."""
    def __init__(self, pyramid, frame_delay=0.2):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

        # Knobs to change for effect
        self.knobs.register('Low Saturation', ValueKnob(default=0.8, min=0.0, max=1.0, step=0.05))
        self.knobs.register('High Saturation', ValueKnob(default=1.0, min=0.0, max=1.0, step=0.05))
        self.knobs.register('Steps', ValueKnob(default=3, min=1, max=8, step=1))
        self.knobs.register('Base Color', HSVKnob(default=HSV(351.0/360.0, 1.0, 1.0)))

        # Not sure of the proper formula for this, but allows running on normal or mega triangle.
        self.max_distance = 0
        while self.grid.select(inset(self.max_distance)):
            self.max_distance += 1

    @staticmethod
    def description() -> str:
        return 'pulse where saturation gently fluctuates'

    def next_frame(self):
        while True:
            # 1. Paint the triangle the color
            color = self.knobs['Base Color']
            color.s = self.knobs['Low Saturation']
            self.grid.set(every, color)
            yield self.frame_delay

            # 2. From center outward, adjust the saturation up like a wave
            for distance in range(self.max_distance, -1, -1):
                self.saturate_from_distance(distance,
                                            color=self.knobs['Base Color'],
                                            steps=self.knobs['Steps'],
                                            low_saturation=self.knobs['Low Saturation'],
                                            high_saturation=self.knobs['High Saturation'])
                yield self.frame_delay

            # 3. From center outward, adjust the saturation down like a wave
            for distance in range(self.max_distance, -1, -1):
                self.saturate_from_distance(distance,
                                            color=self.knobs['Base Color'],
                                            steps=self.knobs['Steps'],
                                            low_saturation=self.knobs['Low Saturation'],
                                            high_saturation=self.knobs['High Saturation'],
                                            adjust_down=True)
                yield self.frame_delay

    def saturate_from_distance(self, distance, color, steps, low_saturation, high_saturation, adjust_down=False):
        """Saturates color steps from a distance (from center) outward."""
        saturation_delta = (high_saturation - low_saturation) / steps
        if adjust_down:
            saturation_delta *= -1

        for step in range(0, steps + 1):
            for i in range(step + 1):
                saturation = low_saturation if saturation_delta > 0 else high_saturation
                saturation = saturation + (saturation_delta * (step - i))
                color.s = saturation

                if distance - i < 0:
                    continue
                self.grid.set(inset(distance - i), color)

from path import Path


class Drone:
    def __init__(self, num: int) -> None:
        self.num: int = num
        self.route: list[Path] = []
        self.start_time: int = 0
        self.current_step: int = 0
        self.turns_left: int = 0
        self.is_finished: bool = False

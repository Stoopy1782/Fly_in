from enum import Enum
import webcolors
from webcolors import IntegerRGB


class ZoneError(Exception):
    def __str__(self) -> str:
        return "Zone parameter type is invalid\n"


class Zone:
    class Zone_type(Enum):
        NORMAL = "normal"
        BLOCKED = "blocked"
        RESTRICTED = "restricted"
        PRIORITY = "priority"

    def __init__(self, param: str):
        self.type = Zone.Zone_type.NORMAL
        self.color: IntegerRGB
        self.max_drones = 1
        self.x = 0
        self.y = 0
        if " [" in param:
            key, value = param.split(" [", 1)
            # key = hub x y, value = color=...
            self.set_coordinate(key)
            self.set_status(value)
        else:
            self.set_coordinate(param)

    def set_coordinate(self, param: str) -> None:
        parts = param.split()
        if len(parts) < 3:
            raise ZoneError
        self.name = parts[0]
        try:
            self.x = int(parts[1])
            self.y = int(parts[2])
        except Exception:
            raise ZoneError

    def set_status(self, param: str) -> None:
        param = param.rstrip("]")
        options = param.split()
        if not options:
            raise ZoneError

        for opt in options:
            if "=" not in opt:
                raise ZoneError
            name, args = opt.split("=", 1)
            if name == "zone":
                try:
                    self.type = Zone.Zone_type(args)
                except Exception:
                    raise ZoneError
            elif name == "color":
                try:
                    self.color = webcolors.name_to_rgb(args.strip().lower())
                except ValueError:
                    self.color = webcolors.name_to_rgb("white")
            elif name == "max_drones":
                try:
                    n = int(args)
                    if n <= 0:
                        raise ValueError
                    self.max_drones = n
                except ValueError:
                    raise ZoneError
            else:
                raise ZoneError

    def print_color(self, text: str) -> None:
        if self.color is None:
            print(text)
            return
        r, g, b = self.color
        print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

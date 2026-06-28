import sys
import argparse
from zone import Zone
from path import Path
from drone import Drone
import typing
import webcolors


class MapError(Exception):
    def __str__(self) -> str:
        return "Map parameter is invalid\n"


class Manager:
    def __init__(self) -> None:
        self.drones: list[Drone] = []
        self.paths: list[Path] = []
        self.zones: list[Zone] = []
        self.start_name: str = ""
        self.end_name: str = ""
        self.routes: list[list[Path]] = []
        self.start_hub_count = 0
        self.end_hub_count = 0
        self.links: list[list[str]] = []
        self.zone_dict: dict[str, Zone] = {}
        self.cost_dict: dict[tuple[Path, ...], float] = {}
        self.length_dict: dict[tuple[Path, ...], float] = {}

    def read_file(self, file: str) -> None:
        try:
            with open(file, "r") as f:
                for line in f:

                    if not line.strip() or line.startswith("#"):
                        continue

                    if (": " in line):
                        key, value = line.split(": ", 1)
                        # key = start_hub, value = start 0 0 [...]
                        key = key.strip()
                        value = value.strip()

                        if key == "nb_drones":
                            try:
                                n_drone = int(value)
                                if n_drone <= 0:
                                    raise ValueError
                            except ValueError:
                                raise MapError
                            self.add_drone(n_drone)
                        elif key == "connection":
                            path = Path(value)
                            start_z = self.zone_dict.get(path.start)
                            end_z = self.zone_dict.get(path.end)

                            if start_z and start_z.type.value == "blocked" or \
                               end_z and end_z.type.value == "blocked":
                                continue

                            link = sorted((path.start, path.end))
                            if link in self.links:
                                raise MapError
                            self.links.append(link)
                            self.paths.append(path)
                        elif key == "start_hub":
                            self.start_name = value.split()[0]
                            self.zone_dict[self.start_name] = Zone(value)
                            if self.start_hub_count != 0:
                                raise MapError
                            self.start_hub_count += 1
                        elif key == "end_hub":
                            self.end_name = value.split()[0]
                            self.zone_dict[self.end_name] = Zone(value)
                            self.end_hub_count += 1
                        elif key == "hub":
                            n_zone = Zone(value)
                            self.zone_dict[n_zone.name] = n_zone
                        else:
                            raise MapError

            if self.start_hub_count != 1 or self.end_hub_count != 1:
                raise MapError
            else:
                self.routes = self.find_routes(
                    self.start_name, self.end_name, [], [])

        except Exception as e:
            print(e)
            sys.exit(1)

    def find_routes(
        self, current: str, goal: str, visited: list[str], route: list[Path]
    ) -> list[list[Path]]:
        if current in visited:
            return []
        if current == goal:
            return [route]

        result = []
        for p in self.paths:
            if p.start == current:
                result += self.find_routes(
                    p.end, goal, visited + [current], route + [p])
        return result

    def mesaure_route(self) -> None:
        for route in self.routes:
            # path1, path2, ...
            sum_cost = 0.0
            for path in route:
                end_zone = self.zone_dict[path.end]
                if end_zone.type.value == "normal":
                    sum_cost += 1.0
                elif end_zone.type.value == "priority":
                    sum_cost += 0.99
                elif end_zone.type.value == "restricted":
                    sum_cost += 2.0
            route_key = tuple(route)
            self.cost_dict[route_key] = sum_cost

    def decide_route(self) -> None:
        if not self.routes:
            return
        best_route = min(self.routes, key=lambda r: self.cost_dict[tuple(r)])
        i: int = 1
        for drone in self.drones:
            drone.route = best_route
            drone.start_time = i
            i += 1
        turn = 1

        finished_count = 0
        total_drones = len(self.drones)

        while finished_count < total_drones:
            logs = []
            for drone in self.drones:
                if turn <= drone.start_time:
                    continue
                if drone.current_step >= len(drone.route):
                    continue

                path = drone.route[drone.current_step]
                dest_zone = typing.cast(Zone, self.zone_dict.get(path.end))
                start_zone = typing.cast(Zone, self.zone_dict.get(path.start))
                if dest_zone.type.value == "restricted":
                    if drone.turns_left == 0:
                        drone.turns_left = 1
                        if start_zone.color == "rainbow":
                            cl_tx1 = self.ret_rainbow(
                                f"D{drone.num}-{path.start}")
                        else:
                            r1, g1, b1 = start_zone.color
                            tx1 = f"D{drone.num}-{path.start}"
                            cl_tx1 = f"\033[38;2;{r1};{g1};{b1}m{tx1}\033[0m"
                        if dest_zone.color == "rainbow":
                            cl_tx2 = self.ret_rainbow(f"-{path.end}")
                        else:
                            r2, g2, b2 = dest_zone.color
                            tx2 = f"-{path.end}"
                            cl_tx2 = f"\033[38;2;{r2};{g2};{b2}m{tx2}\033[0m"
                        logs.append(cl_tx1+cl_tx2)
                        continue

                drone.turns_left = 0
                text = f"D{drone.num}-{path.end}"
                if dest_zone.color == "rainbow":
                    color_text = self.ret_rainbow(text)
                else:
                    r, g, b = dest_zone.color
                    color_text = f"\033[38;2;{r};{g};{b}m{text}\033[0m"
                logs.append(color_text)
                drone.current_step += 1
                if drone.current_step == len(drone.route):
                    finished_count += 1
            if logs:
                print(" ".join(logs))
            turn += 1

    def add_drone(self, num: int) -> None:
        i = 1
        while num >= i:
            d = Drone(i)
            self.drones.append(d)
            i += 1

    def ret_rainbow(self, text: str) -> str:
        colors = ["red", "orange", "yellow", "green",
                  "blue", "indigo", "violet"]
        ret = ""
        for i in range(len(text)):
            index = i % 7
            r, g, b = webcolors.name_to_rgb(colors[index])
            ret += f"\033[38;2;{r};{g};{b}m{text[i]}\033[0m"
        return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_path",
        default="maps/easy/01_linear_path.txt"
    )
    args = parser.parse_args()
    play = Manager()
    play.read_file(args.file_path)
    play.mesaure_route()
    play.decide_route()

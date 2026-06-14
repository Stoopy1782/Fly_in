import sys
import argparse
from zone import Zone
from path import Path
from drone import Drone


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
        self.routes: list[list[str]] = []
        self.start_hub_count = 0
        self.end_hub_count = 0
        self.links: list[list[str]] = []

    def read_file(self, file: str) -> None:
        try:
            with open(file, "r") as f:
                for line in f:

                    if not line.strip() or line.startswith("#"):
                        continue

                    if (": " in line):
                        key, value = line.split(": ", 1)
                        key = key.strip()
                        value = value.strip()

                        if key == "nb_drones":
                            try:
                                n_value = int(value)
                                if n_value <= 0:
                                    raise ValueError
                            except ValueError:
                                raise MapError
                            for _ in range(n_value):
                                self.add_drone()
                        elif key == "connection":
                            path = Path(value)
                            link = sorted((path.start, path.end))
                            if link in self.links:
                                raise MapError
                            self.links.append(link)
                            self.paths.append(path)
                        elif key == "start_hub":
                            self.start_name = value.split()[0]
                            self.zones.append(Zone(value))
                            if self.start_hub_count != 0:
                                raise MapError
                            self.start_hub_count += 1
                        elif key == "end_hub":
                            self.end_name = value.split()[0]
                            self.zones.append(Zone(value))
                            if self.end_hub_count != 0:
                                raise MapError
                            self.end_hub_count += 1
                        else:
                            n_zone = Zone(value)
                            self.zones.append(n_zone)

            if self.start_name and self.end_name:
                self.routes = self.find_routes(self.start_name, self.end_name)

        except Exception as e:
            print(e)
            sys.exit(1)

    def find_routes(
        self, current: str, goal: str, path: list[str] = []
    ) -> list[list[str]]:
        if current in path:
            return []
        path = path + [current]
        if current == goal:
            return [path]
        result = []
        for p in self.paths:
            if current in p.graph:
                for neighbor in p.graph[current]:
                    result += self.find_routes(neighbor, goal, path)
        return result

    def add_drone(self) -> None:
        d = Drone()
        self.drones.append(d)

    def show_stats(self) -> None:
        print("=" * 40)
        print("       SIMULATION STATUS REPORT       ")
        print("=" * 40)

        # 1. ドローン情報の出力
        print(f"🛸 [Drones] Total: {len(self.drones)}")
        print("-" * 40)

        # 2. パス（ルート）情報の出力
        print(f"🛣️  [Routes] Total: {len(self.routes)}")
        for i, route in enumerate(self.routes, 1):
            print(f"  Route {i:02d}: {' -> '.join(route)}")
        print("-" * 40)

        # 3. エリア（Zone）情報の出力
        print(f"📍 [Zones] Total: {len(self.zones)}")
        for i, zone in enumerate(self.zones, 1):
            # 座標の文字列整形
            coord_str = f"({zone.x}, {zone.y})"

            # オプションの文字列整形
            color_str = zone.color if zone.color else "None"

            max_d = zone.max_drones
            print(f"  Zone {i:02d}:")
            print(f"    - Coordinate : {coord_str}")
            print(f"    - Type       : {zone.type.value}")
            print(f"    - Color      : {color_str}")
            print(f"    - Max Drones : {max_d}")
            zone.print_color('Color')
            print()
        print("=" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_path",
        default="maps/easy/01_linear_path.txt"
    )
    args = parser.parse_args()
    play = Manager()
    play.read_file(args.file_path)
    play.show_stats()

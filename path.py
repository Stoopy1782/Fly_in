class PathError(Exception):
    def __str__(self) -> str:
        return "Path parameter type is invalid\n"


class Path:
    def __init__(self, param: str) -> None:
        self.capacity = 1
        self.start = ""
        self.end = ""
        self.graph: dict[str, list[str]] = {}
        if " [" in param:
            key, value = param.split(" [", 1)
            # key = start-junction, value = max_link_capacity=?]
            self.set_path(key)
            self.set_status(value)
        else:
            self.set_path(param)

    def set_path(self, connection: str) -> None:
        nodes = connection.split("-")
        if len(nodes) != 2:
            raise PathError
        self.start = nodes[0]
        self.end = nodes[1]
        self.graph.setdefault(self.start, []).append(self.end)

    def set_status(self, option: str) -> None:
        cap = option.split("max_link_capacity=")
        if len(cap) != 2:
            raise PathError
        try:
            capacity = int(cap[1].rstrip("]"))
            if capacity >= 1:
                self.capacity = capacity
            else:
                raise ValueError
        except ValueError:
            raise PathError

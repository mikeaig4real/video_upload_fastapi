from typing_extensions import Literal

Unit = Literal["B", "KB", "MB", "GB", "TB"]

unitMap: dict[Unit, int] = {
    "B": 1,
    "KB": 1024,
    "MB": 1024**2,
    "GB": 1024**3,
    "TB": 1024**4,
}


def convertSize(value: int, fromUnit: Unit, toUnit: Unit) -> float | int:
    if fromUnit not in unitMap or toUnit not in unitMap:
        raise ValueError(f"Invalid unit. Allowed: {list(unitMap.keys())}")
    return value * unitMap[fromUnit] / unitMap[toUnit]

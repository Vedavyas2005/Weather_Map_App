def temp_label(units: str) -> str:
    return "°C" if units == "metric" else "°F"

def speed_label(units: str) -> str:
    return "m/s" if units == "metric" else "mph"

def convert_temp(n: float, from_units: str, to_units: str) -> float:
    if n is None or from_units == to_units:
        return n
    if from_units == "metric" and to_units == "imperial":
        return n * 9/5 + 32
    if from_units == "imperial" and to_units == "metric":
        return (n - 32) * 5/9
    return n

def convert_wind_speed(n: float, from_units: str, to_units: str) -> float:
    if n is None or from_units == to_units:
        return n
    if from_units == "metric" and to_units == "imperial":
        return n * 2.2369362920544
    if from_units == "imperial" and to_units == "metric":
        return n / 2.2369362920544
    return n

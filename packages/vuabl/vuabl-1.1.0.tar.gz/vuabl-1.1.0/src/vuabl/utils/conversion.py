
def get_size_prefix(sizeStr: str) -> str:
    sizePrefix: str = sizeStr[-2]

    if sizePrefix.isnumeric():
        return ""

    return sizePrefix


def get_size_prefix_power(sizePrefix: str) -> int:
    sizePrefixes: list[str] = [ "", "k", "m", "g", "t", "p", "e", "z", "y" ]
    sizePrefix = sizePrefix.lower()

    for index, prefix in enumerate(sizePrefixes):
        if sizePrefix == prefix:
            return index

    return 0


def get_size_unit_power(sizeStr: str) -> int:
    sizePrefix: str = get_size_prefix(sizeStr)
    return get_size_prefix_power(sizePrefix)


def size_to_bytes(sizeStr: str) -> int:
    sizeStr = sizeStr.replace(",", ".")
    power: int = get_size_unit_power(sizeStr)

    if power < 1:
        sizeNumber = sizeStr[:-1]
    else:
        sizeNumber = sizeStr[:-2]

    return int(float(sizeNumber) * pow(1024, power))



def get_size_power(size: int) -> int:
    power: int = 0

    while size >= 1024:
        size /= 1024
        power += 1

    return power


def get_size_power_prefix(power: int) -> str:
    sizePrefixes: list[str] = [ "", "K", "M", "G", "T", "P", "E", "Z", "Y" ]

    if power < 0 or power >= len(sizePrefixes):
        return ""

    return sizePrefixes[power]


def get_full_size_power_postfix(power: int) -> str:
    return f"{get_size_power_prefix(power)}B"


def bytes_to_readable_size(size: int) -> str:
    power: int = get_size_power(size)
    fractSize: float = size / pow(1024, power)
    return f"{fractSize:.2f}{get_full_size_power_postfix(power)}"



def to_layout_id(name: str) -> str:
    return name.lower().replace(" ", "-")

from vuabl.data.asset import Asset
from re import Match
import vuabl.utils.conversion as conversion
import vuabl.parsing.asset_type as pasttp
import re



def is_param(line: str, paramName: str) -> bool:
    return re.match(rf"^\s*{paramName}:[ ]{{0,1}}.+", line)



def get_integer_param(line: str, paramName: str) -> int:
    match: Match = re.search(rf"^\s*{paramName}:[ ]{{0,1}}(\d+).*", line)

    if match and len(match.groups()) > 0:
        return int(match.group(1))

    return 0


def get_size_param(line: str, paramName: str) -> int:
    match: Match = re.search(rf"^\s*{paramName}:[ ]{{0,1}}((\d+[,.]){{0,1}}\d+[KkMmGgTtPpEe]{{0,1}}[Bb]).*", line)
    
    if match and len(match.groups()) > 0:
        return conversion.size_to_bytes(match.group(1))
    
    return 0


def get_string_param(line: str, paramName: str) -> str:
    match: Match = re.search(rf"^\s*{paramName}:[ ]{{0,1}}([^,)]+)", line)

    if match and len(match.groups()) > 0:
        return match.group(1)

    return ""


def get_strings_list_param(line: str, paramName: str) -> list:
    match: Match = re.search(rf"^\s*{paramName}:[ ]{{0,1}}(.+)", line)

    if match and len(match.groups()) > 0:
        return match.group(1).split(", ")

    return []


def get_assets_list_param(line: str, paramName: str) -> list:
    paths: list[str] = get_strings_list_param(line, paramName)
    return [Asset(path=path, assetType=pasttp.get_asset_type(path)) for path in paths]



def is_header_contains_param(header: str, paramName: str) -> bool:
    return re.match(rf"[(,][ ]{{0,1}}{paramName}:.+", header)


def get_header_integer_param(header: str, paramName: str) -> int:
    match: Match = re.search(rf"[(,][ ]{{0,1}}{paramName}:[ ]{{0,1}}(\d+)[,)]", header)
    
    if match and len(match.groups()) > 0:
        return int(match.group(1))

    return 0


def get_header_size_param(header: str, paramName: str) -> int:
    match: Match = re.search(rf"[(,][ ]{{0,1}}{paramName}:[ ]{{0,1}}((\d+[,.]){{0,1}}\d+[KkMmGgTtPpEe]{{0,1}}[Bb])[,)]", header)

    if match and len(match.groups()) > 0:
        return conversion.size_to_bytes(match.group(1))

    return 0


def get_header_string_param(header: str, paramName: str) -> str:
    match: Match = re.search(rf"[(,][ ]{{0,1}}{paramName}:[ ]{{0,1}}([^,)]+)[,)]", header)

    if match and len(match.groups()) > 0:
        return match.group(1)

    return ""



def get_bundles_count(header: str) -> int:
    return get_header_integer_param(header, "Bundles")


def get_explicit_asset_count(header: str) -> int:
    return get_header_integer_param(header, "Explicit Asset Count")


def get_file_index(header: str) -> int:
    return get_header_integer_param(header, "File Index")


def get_total_size(header: str) -> int:
    return get_header_size_param(header, "Total Size")


def get_asset_bundle_object_size(header: str) -> int:
    return get_header_size_param(header, "Asset Bundle Object Size")


def get_size_from_objects(header: str) -> int:
    return get_header_size_param(header, "Size from Objects")


def get_size_from_streamed_data(header: str) -> int:
    return get_header_size_param(header, "Size from Streamed Data")


def get_size(header: str) -> int:
    return get_header_size_param(header, "Size")


def get_compression(header: str) -> str:
    return get_header_string_param(header, "Compression")


def get_addressable_name(header: str) -> str:
    return get_header_string_param(header, "Addressable Name")



def get_intent(line: str) -> int:
    return len(re.search(r"^(\s*)", line).group(1))
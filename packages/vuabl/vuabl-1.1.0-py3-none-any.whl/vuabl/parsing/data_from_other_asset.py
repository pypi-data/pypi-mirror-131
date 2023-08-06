from vuabl.data.data_from_other_asset import DataFromOtherAsset
from vuabl.utils.layout_reader import LayoutReader
import vuabl.parsing.parameters as pparamrs
import vuabl.parsing.asset_type as pasttp
import re



def is_data_from_other_assets_header(line: str) -> bool:
    return re.match(r"^\s*Data From Other Assets.*", line)



def parse_file_data_from_other_asset(reader: LayoutReader) -> DataFromOtherAsset:
    data: DataFromOtherAsset = DataFromOtherAsset()
    intent: int = pparamrs.get_intent(reader.currentLine())

    data.path = re.search(r"^\s*([^(]+)\(", reader.currentLine()).group(1).rstrip()
    data.assetType = pasttp.get_asset_type(data.path)
    data.size = pparamrs.get_size(reader.currentLine())
    data.sizeFromObjects = pparamrs.get_size_from_objects(reader.currentLine())
    data.sizeFromStreamedData = pparamrs.get_size_from_streamed_data(reader.currentLine())
    data.objectCount = pparamrs.get_header_integer_param(reader.currentLine(), "Object Count")

    try:
        while True:
            line: str = reader.nextLine()

            if pparamrs.get_intent(line) <= intent:
                break
            elif pparamrs.is_param(line, "Referencing Assets"):
                data.referencingAssets = pparamrs.get_assets_list_param(line, "Referencing Assets")

    except StopIteration:
        pass

    return data


def parse_file_data_from_other_assets(reader: LayoutReader) -> list:
    data: list[DataFromOtherAsset] = []
    intent: int = pparamrs.get_intent(reader.currentLine())

    try: 
        isNext: bool = True

        while True:
            line: str = reader.currentLine()

            if isNext:
                line = reader.nextLine()

            curIntent = pparamrs.get_intent(line)

            if curIntent <= intent:
                break
            elif curIntent == intent + 1:
                data.append(parse_file_data_from_other_asset(reader))
                isNext = False

    except StopIteration:
        pass

    return data

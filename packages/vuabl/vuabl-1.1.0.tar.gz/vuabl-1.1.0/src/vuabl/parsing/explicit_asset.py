from vuabl.data.explicit_asset import ExplicitAsset
from vuabl.utils.layout_reader import LayoutReader
import vuabl.parsing.parameters as pparams
import vuabl.parsing.asset_type as pasttp
import re



def is_explicit_assets_header(line: str) -> bool:
    return re.match(r"^\s*Explicit Assets[:]{0,1}.*", line)



def parse_archive_explicit_asset(reader: LayoutReader) -> ExplicitAsset:
    asset: ExplicitAsset = ExplicitAsset()
    intent: int = pparams.get_intent(reader.currentLine())

    asset.path = re.search(r"^\s*([^(]+)\(", reader.currentLine()).group(1).rstrip()
    asset.assetType = pasttp.get_asset_type(asset.path)
    asset.totalSize = pparams.get_total_size(reader.currentLine())
    asset.sizeFromObjects = pparams.get_size_from_objects(reader.currentLine())
    asset.sizeFromStreamedData = pparams.get_size_from_streamed_data(reader.currentLine())
    asset.fileIndex = pparams.get_file_index(reader.currentLine())
    asset.addressableName = pparams.get_addressable_name(reader.currentLine())

    try:
        while True: 
            line: str = reader.nextLine()

            if pparams.get_intent(line) <= intent: 
                break
            if pparams.is_param(line, "Internal References"):
                asset.internalReferences = pparams.get_assets_list_param(line, "Internal References")

    except StopIteration:
        pass

    return asset



def parse_archive_explicit_assets(reader: LayoutReader) -> list:
    assets: list[ExplicitAsset] = []
    intent: int = pparams.get_intent(reader.currentLine())

    try:
        isNext: bool = True

        while True:
            line: str = reader.currentLine()

            if isNext:
                line = reader.nextLine()

            if pparams.get_intent(line) <= intent:
                break
            else:
                assets.append(parse_archive_explicit_asset(reader))
                isNext = False

    except StopIteration:
        pass

    return assets
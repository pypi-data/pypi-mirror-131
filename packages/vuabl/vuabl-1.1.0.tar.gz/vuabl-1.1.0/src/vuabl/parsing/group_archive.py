from vuabl.data.group_archive import GroupArchive
from vuabl.utils.layout_reader import LayoutReader
import vuabl.parsing.parameters as pparams
import vuabl.parsing.file as pfl
import vuabl.parsing.explicit_asset as pexplast
import re



def is_group_archive_header(line: str) -> bool:
    return re.match(r"^\s*Archive .+", line)



def parse_group_archive(reader: LayoutReader) -> GroupArchive:
    archive: GroupArchive = GroupArchive()
    intent: int = pparams.get_intent(reader.currentLine())

    archive.name = re.search(r"^\s*Archive (.+) \(.*", reader.currentLine()).group(1)

    archive.size = pparams.get_size(reader.currentLine())
    archive.assetBundleObjectSize = pparams.get_asset_bundle_object_size(reader.currentLine())
    archive.compression = pparams.get_compression(reader.currentLine())

    try:
        isNext: bool = True

        while True:
            line: str = reader.currentLine()

            if isNext:
                line = reader.nextLine()

            if pparams.get_intent(line) <= intent:
                break
            elif pexplast.is_explicit_assets_header(line):
                archive.explicitAssets = pexplast.parse_archive_explicit_assets(reader)
                isNext = False
            elif pfl.is_files_header(line):
                archive.files = pfl.parse_group_archive_files(reader)
                isNext = False

    except StopIteration:
        pass

    return archive
from vuabl.data.group import Group
from vuabl.utils.layout_reader import LayoutReader
import vuabl.parsing.parameters as pparams
import vuabl.parsing.group_archive as pgrarch
import re



def is_group_header(line: str) -> bool:
    return re.match(r"^\s*Group .+", line)



def parse_group(reader: LayoutReader) -> Group:
    group: Group = Group()
    intent: int = pparams.get_intent(reader.currentLine())
    
    group.name = re.search(r"^\s*Group (.+) \(.*", reader.currentLine()).group(1)
    group.bundlesCount = pparams.get_bundles_count(reader.currentLine())
    group.explicitAssetCount = pparams.get_explicit_asset_count(reader.currentLine())
    group.totalSize = pparams.get_total_size(reader.currentLine())

    try:
        isNext: bool = True

        while True:
            line: str = reader.currentLine()

            if isNext:
                line = reader.nextLine()

            if pparams.get_intent(line) <= intent:
                break
            elif pgrarch.is_group_archive_header(line):
                group.archives.append(pgrarch.parse_group_archive(reader))
                isNext = False

    except StopIteration:
        pass

    return group
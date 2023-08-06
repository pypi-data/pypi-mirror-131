from vuabl.data.summary import Summary
from vuabl.utils.layout_reader import LayoutReader
import vuabl.parsing.parameters as pparams
import re



def is_summary_header(line: str) -> bool:
    return re.match(r"^\s*Summary.*", line)



def parse_summary(reader: LayoutReader) -> Summary:
    summary: Summary = Summary()
    intent: int = pparams.get_intent(reader.currentLine())

    try:
        while True:
            line: str = reader.nextLine()

            if pparams.get_intent(line) <= intent:
                break
            elif pparams.is_param(line, "Addressable Groups"):
                summary.groupsCount = pparams.get_integer_param(line, "Addressable Groups")
            elif pparams.is_param(line, "Total Build Size"):
                summary.totalBuildSize = pparams.get_size_param(line, "Total Build Size")
            elif pparams.is_param(line, "Total MonoScript Size"):
                summary.totalMonoScriptSize = pparams.get_size_param(line, "Total MonoScript Size")
            elif pparams.is_param(line, "Total AssetBundle Object Size"):
                summary.totalAssetBundleObjectSize = pparams.get_size_param(line, "Total AssetBundle Object Size")
    
    except StopIteration:
        pass

    return summary
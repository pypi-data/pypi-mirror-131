from vuabl.data.asset_data import AssetData
from vuabl.data.build_layout import BuildLayout
from vuabl.utils.layout_reader import LayoutReader
import vuabl.parsing.parameters as pparams
import vuabl.parsing.summary as psummary
import vuabl.parsing.group as pgroup



def parse_build_layout(reader: LayoutReader) -> BuildLayout:
    layout: BuildLayout = BuildLayout()
    
    try:
        isNext: bool = True

        while True:
            line: str = reader.currentLine()

            if isNext:
                line = reader.nextLine()

            isNext = True

            if pparams.is_param(line, "Unity Version"):
                layout.environment.unityVersion = pparams.get_string_param(line, "Unity Version")
            elif pparams.is_param(line, "com.unity.addressables"):
                layout.environment.addressablesPackageVersion = pparams.get_string_param(line, "com.unity.addressables")
            elif psummary.is_summary_header(line):
                layout.summary = psummary.parse_summary(reader)
                isNext = False
            elif pgroup.is_group_header(line):
                layout.groups.append(pgroup.parse_group(reader))
                isNext = False

    except StopIteration:
        pass

    layout.assetsData = build_assets_data(layout)
    layout.groups.sort(key=lambda entry:entry.name)

    return layout


def read_build_layout(path: str) -> BuildLayout:
    reader: LayoutReader = LayoutReader(path)
    layout: BuildLayout = parse_build_layout(reader)
    layout.environment.layoutPath = path

    reader.close()
    return layout



def build_assets_data(layout: BuildLayout) -> dict:
    data: dict[str, AssetData] = {}

    for group in layout.groups:
        for archive in group.archives:
            for explicitAsset in archive.explicitAssets:
                if not explicitAsset.path in data:
                    data[explicitAsset.path] = AssetData(asset=explicitAsset, size=explicitAsset.totalSize)

                data[explicitAsset.path].referencedByGroups.add(group.name)
                data[explicitAsset.path].referencedByArchives.add(archive.name)

            for file in archive.files:
                for dataFromOtherAsset in file.dataFromOtherAssets:
                    if not dataFromOtherAsset.path in data:
                        data[dataFromOtherAsset.path] = AssetData(asset=dataFromOtherAsset, size=dataFromOtherAsset.size)
                    
                    data[dataFromOtherAsset.path].referencedByGroups.add(group.name)
                    data[dataFromOtherAsset.path].referencedByArchives.add(archive.name)

                    for referencingAsset in dataFromOtherAsset.referencingAssets:
                        data[dataFromOtherAsset.path].referencedByAssets.add(referencingAsset)

    return data
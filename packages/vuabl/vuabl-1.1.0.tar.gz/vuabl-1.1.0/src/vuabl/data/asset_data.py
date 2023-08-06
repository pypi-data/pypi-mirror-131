from dataclasses import dataclass, field
from vuabl.data.asset import Asset


@dataclass
class AssetData:
    asset: Asset = Asset()
    size: int = 0
    referencedByAssets: set = field(default_factory=set)
    referencedByGroups: set = field(default_factory=set)
    referencedByArchives: set = field(default_factory=set)



def compare(a: AssetData, b: AssetData) -> int:
    aPathLower: str = a.asset.path.lower()
    bPathLower: str = b.asset.path.lower()

    if a.size < b.size:
        return 1
    elif a.size > b.size:
        return -1
    elif aPathLower < bPathLower:
        return -1
    elif a.asset.path > bPathLower:
        return 1

    return 0


def compare_with_duplicates(a: AssetData, b: AssetData) -> int:
    aPathLower: str = a.asset.path.lower()
    bPathLower: str = b.asset.path.lower()
    aTotalSize: int = a.size * len(a.referencedByArchives)
    bTotalSize: int = b.size * len(b.referencedByArchives)

    if aTotalSize < bTotalSize:
        return 1
    elif aTotalSize > bTotalSize:
        return -1
    elif aPathLower < bPathLower:
        return -1
    elif a.asset.path > bPathLower:
        return 1

    return 0

from dataclasses import dataclass
from vuabl.data.asset_type import AssetType



@dataclass
class Asset:
    path: str = ""
    assetType: AssetType = AssetType.Other


    def __hash__(self) -> int:
        return hash(self.path)

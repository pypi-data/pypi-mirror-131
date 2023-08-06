from dataclasses import dataclass, field
from vuabl.data.asset import Asset



@dataclass
class DataFromOtherAsset(Asset):
    size: int = 0
    sizeFromObjects: int = 0
    sizeFromStreamedData: int = 0
    objectCount: int = 0
    referencingAssets: list = field(default_factory=list)
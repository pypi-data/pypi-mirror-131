from dataclasses import dataclass, field



@dataclass
class GroupArchive:
    name: str = ""
    size: int = 0
    assetBundleObjectSize: int = 0
    compression: str = ""
    explicitAssets: list = field(default_factory=list)
    files: list = field(default_factory=list)

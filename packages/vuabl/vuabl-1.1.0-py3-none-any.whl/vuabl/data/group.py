from dataclasses import dataclass, field



@dataclass
class Group:
    name: str = ""
    archives: list = field(default_factory=list)
    totalSize: int = 0
    bundlesCount: int = 0
    explicitAssetCount: int = 0

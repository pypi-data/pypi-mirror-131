from dataclasses import dataclass, field



@dataclass
class File:
    index: int = 0
    monoScriptsCount: int = 0
    monoScroptSize: int = 0
    preloadInfoSize: int = 0
    dataFromOtherAssets: list = field(default_factory=list)

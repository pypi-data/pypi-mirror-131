from dataclasses import dataclass, field
from vuabl.data.environment import Environment
from vuabl.data.summary import Summary



@dataclass
class BuildLayout:
    environment: Environment = Environment()
    summary: Summary = Summary()
    groups: list = field(default_factory=list)
    assetsData: dict = field(default_factory=dict)  # path -> AssetData

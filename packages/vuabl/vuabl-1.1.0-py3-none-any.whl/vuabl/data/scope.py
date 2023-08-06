from enum import Enum



class Scope(Enum):
    Global = 0
    Summary = 1
    Group = 2
    Archive = 100
    ExplicitAssets = 200
    ExplicitAsset = 201
    Files = 300 
    File = 301
    DataFromOtherAssets = 320
    DataFromOtherAsset = 321

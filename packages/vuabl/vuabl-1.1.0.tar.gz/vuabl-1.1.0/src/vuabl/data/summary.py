from dataclasses import dataclass



@dataclass
class Summary:
    groupsCount: int = 0
    totalBuildSize: int = 0
    totalMonoScriptSize: int = 0
    totalAssetBundleObjectSize: int = 0

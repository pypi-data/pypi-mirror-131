from dataclasses import dataclass



@dataclass
class Environment:
    layoutPath: str = ""
    unityVersion: str = ""
    addressablesPackageVersion: str = 0

from vuabl.data.asset_type import AssetType
import re



def get_asset_type(path: str) -> AssetType:
    path = path.rstrip().lower()

    if re.match(r".+\.((png)|(jpg)|(bmp)|(exr)|(gif)|(hdr)|(iff)|(pict)|(psd)|(tga)|(tiff))", path):
        return AssetType.Texture
    elif re.match(r".+\.((aif)|(wav)|(mp3)|(ogg))", path):
        return AssetType.Audio
    elif re.match(r".+\.((asf)|(avi)|(dv)|(m4v)|(mov)|(mp4)|(mpg)|(mpeg)|(ogv)|(vp8)|(webm)|(wmv))", path):
        return AssetType.Video
    elif re.match(r".+\.prefab", path):
        return AssetType.Prefab
    elif re.match(r".+\.unity", path):
        return AssetType.Scene
    elif re.match(r".+\.mat", path):
        return AssetType.Material
    elif re.match(r".+\.((fbx)|(dae)|(3ds)|(dxf)|(obj))", path):
        return AssetType.Model
    elif re.match(r".+\.((ttf)|(otf))", path):
        return AssetType.Font
    elif re.match(r".+\.asset", path):
        return AssetType.ScriptableObject

    return AssetType.Other


def asset_type_to_category_name(assetType: AssetType) -> str:
    if assetType == AssetType.Texture:
        return "Textures"
    elif assetType == AssetType.Audio:
        return "Audio"
    elif assetType == AssetType.Video:
        return "Video"
    elif assetType == AssetType.Prefab:
        return "Prefabs"
    elif assetType == AssetType.Scene:
        return "Scenes"
    elif assetType == AssetType.Material:
        return "Materials"
    elif assetType == AssetType.Model:
        return "Models"
    elif assetType == AssetType.Font:
        return "Fonts"
    elif assetType == AssetType.ScriptableObject:
        return "Scriptable Objects"

    return "Other"
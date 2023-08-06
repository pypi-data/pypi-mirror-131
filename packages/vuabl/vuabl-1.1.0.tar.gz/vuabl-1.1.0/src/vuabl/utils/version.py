import pkg_resources


def get_version() -> str:
    return pkg_resources.get_distribution("vuabl").version

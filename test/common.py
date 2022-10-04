import platform


def is_darwin() -> bool:
    return platform.system() == 'Darwin'

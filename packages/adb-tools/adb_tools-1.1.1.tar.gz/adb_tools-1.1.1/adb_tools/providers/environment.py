from enum import Enum


class Environment(Enum):
    D1 = 0
    D2 = 1
    T0 = 2
    T1 = 3
    T2 = 4
    T99 = 5
    pre = 6
    release = 7


def get_android_env_title(env):
    if env == Environment.pre:
        return "预发布"
    elif env == Environment.T0:
        return "Test-0"
    elif env == Environment.T1:
        return "Test-1"
    elif env == Environment.T2:
        return "Test-2"
    elif env == Environment.T99:
        return "Test-99"
    elif env == Environment.D1:
        return "Dev-1"
    elif env == Environment.D2:
        return "Dev-2"
    else:
        return "Release"


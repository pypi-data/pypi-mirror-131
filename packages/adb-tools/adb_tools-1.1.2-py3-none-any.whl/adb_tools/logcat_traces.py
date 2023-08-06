import os
import subprocess
from time import sleep


def get_android_crash_info(serialno, log_path):
    try:
        cmds = "adb -s %s shell logcat -b crash > %s" % (serialno, log_path)
        proc = subprocess.Popen(
            cmds,
            shell=True,
        )
        sleep(5)
        proc.terminate()
    finally:
        print('获取crash日志成功')


def get_anr_info(serialno, log_path):
    os.system("adb -s %s bugreport %s" % (serialno, log_path))


def clear_device_logcat_info(serialno):
    os.system("adb -s %s shell logcat -b all -c" % serialno)


def get_app_info(serialno, package_name, log_path):
    # 优先级不低于“警告”的所有标记的所有 含指定包名的 日志消息：
    os.system("adb -s %s shell logcat *:W | grep -i %s > %s" % (serialno, package_name, log_path))


if __name__ == "__main__":
    # clear_device_logcat_info('52dc62d9')
    get_anr_info('52dc62d9', '/Users/zhuhuiping/Desktop/脚本/bugreport106')
    # get_android_crash_info('52dc62d9', '/Users/zhuhuiping/zhuhuipingDesktop/脚本/crash105.log')

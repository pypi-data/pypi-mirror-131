import os
import subprocess
import time

from adb_tools.providers.custom_exception import *
from adb_tools.providers.environment import Environment


def adb_install_apk(serialno, path):
    # 覆盖安装
    cmds = "adb -s %s install -d -r %s" % (serialno, path)
    proc = subprocess.Popen(
        cmds,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.wait()
    if proc.returncode == 0:
        print('安装成功')
    else:
        buff = proc.stdout.readline()
        print(proc.stderr.readlines())
        raise InstallApplicationError((buff, proc.stderr.readlines()))


def adb_install_apk_to_all_devices(path):
    sh_path = os.path.join(os.getcwd(), 'adb/adb_install.sh')
    print(sh_path)
    os.popen(r"chmod u+x %s" % sh_path, "r")
    cmds = sh_path+' '+path
    print(cmds)
    proc = subprocess.Popen(
        cmds,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.wait()
    if proc.returncode == 0:
        print('全部安装成功')
    else:
        buff = proc.stdout.readline()
        raise InstallApplicationError((buff, proc.stderr.readlines()))


def adb_uninstall_package(serialno, package):
    cmds = "adb -s %s uninstall %s" % (serialno, package)
    proc = subprocess.Popen(
        cmds,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.wait()
    if proc.returncode == 0:
        print('卸载成功')
    else:
        buff = proc.stdout.readline()
        raise UninstallApplicationError((buff, proc.stderr.readlines()))


def adb_uninstall_package_all_devices(package):
    sh_path = os.path.join(os.getcwd(), 'adb/adb_uninstall.sh')
    os.popen(r"chmod u+x %s" % sh_path, "r")
    cmds = sh_path+' '+package
    print(cmds)
    proc = subprocess.Popen(
        cmds,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.wait()
    if proc.returncode == 0:
        print('全部卸载成功')
    else:
        buff = proc.stdout.readline()
        raise UninstallApplicationError((buff, proc.stderr.readlines()))


def dewu_app_version(serialno, package):
    print(serialno, package)
    f = os.popen(r'adb -s %s shell pm dump %s | grep "versionName"' % (serialno, package), "r")
    out = f.read()
    f.close()
    # 输出结果字符串处理
    print(out)
    return out.split('\n')[0].split('=')[1] if len(out) > 0 else None


def open_native_page(serialno, url, **kwargs):
    argus = ''
    for key in kwargs.keys():
        argus += ' %s %s' % (key, kwargs[key])
    if kwargs == {}:
        os.popen(r'adb -s %s shell am start -n %s' % (serialno, url), "r")
    else:
        os.popen(r'adb -s %s shell am start -n %s -e %s' % (serialno, url, argus))


def open_scheme_page(serialno, url, **kwargs):
    argus = ''
    for key in kwargs.keys():
        argus += ' %s %s' % (key, kwargs[key])
    if kwargs == {}:
        os.popen(r'adb -s %s shell am start -d dewuapp_debug://web/BrowserPage?url=%s' % (serialno, url))
    else:
        os.popen(r'adb -s %s shell am start -d dewuapp_debug://web/BrowserPage?url=%s -e%s' % (serialno, url, argus))


def open_dewu_developer_settings(serialno, package):
    # os.popen(r'adb -s %s shell am start -n %s/%s.modules.developer.NewDebugActivity' % (serialno, package, package), "r")
    open_native_page(serialno, '%s/%s.modules.developer.NewDebugActivity' % (package, package))


def get_app_environment(serialno):
    package = 'com.shizhuang.duapp'
    # 再获取logcat详细信息
    adb_string = r"adb -s %s shell logcat ActivityManager:I %s:D | grep -o '\"host\":.*app.dewu.com\"'" % (serialno, package)
    print(adb_string)
    file_name = 'logcat.text'
    logcat_file = open(file_name, 'w')
    proc = subprocess.Popen(adb_string,
                            shell=True,
                            stdout=logcat_file)

    time.sleep(5)
    proc.terminate()

    with open(file_name, 'r') as f:  #打开文件
        lines = f.readlines() #读取所有行
        buff = lines[-1] if len(lines)>0 else '' #取最后一行

        if 't0-' in buff:
            return Environment.T0
        elif 't1-' in buff:
            return Environment.T1
        elif 't2-' in buff:
            return Environment.T2
        elif 't99-' in buff:
            return Environment.T99
        elif 'd1-' in buff:
            return Environment.D1
        elif 'd2-' in buff:
            return Environment.D2
        elif 'pre-' in buff:
            return Environment.pre
        else:
            return Environment.release


if __name__ == '__main__':
    open_page('a', 'b', c=1, d=2, q=3)
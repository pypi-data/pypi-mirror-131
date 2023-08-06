from datetime import datetime
import os
import re
import zipfile

from adb_tools.providers.anr import ANR
from adb_tools.providers.crash import CRASH


def analyze_anr_info(file_path, anr_start_time=None):
    """
    :param file_path:  anr 文件路径
    :param anr_start_time: 需要解析的anr 开始时间
    :return:
    """
    zipFile = zipfile.ZipFile(file_path, 'r')
    now = datetime.now()
    anr_file_name = ''
    anr_file_time = anr_start_time if anr_start_time is not None else now.strftime('%Y-%m-%d-00-00-00-000')
    for file_name in zipFile.namelist():
        if 'anr_' in file_name:
            time = file_name.split('anr_')[1]
            if time > anr_file_time:
                anr_file_name = file_name
                anr_file_time = time
    # print(anr_file_time)
    if len(anr_file_name) == 0: return
    data = zipFile.read(anr_file_name).decode()
    zipFile.close()
    # 2.解析

    if '"main" prio=5 tid=1 Native' in data:
        anr_reason = data.split('"main" prio=5 tid=1 Native')[1].split('\n\n')[0]
        return ANR(reason=anr_reason, time=anr_file_time)
    else:
        return


def analyze_crash_info(file_path):
    if os.path.getsize(file_path) <= 0:
        return

    f = open(file_path, 'r')
    data = f.read()

    def get_value(key, split_key):
        return data.split(key)[1].split(split_key)[0].strip("'") if len(data.split(key))>1 else None
    f.close()
    title = get_value(' : ', '\n')
    procese = get_value('Process name is', '\n')
    ABI = get_value('ABI: ', '\n')
    time = get_value('Timestamp: ', '\n')
    # fingerprint = get_value("Build fingerprint: '", '/')
    fingerprint = data.split("Build fingerprint: '")[1].split('/') if len(data.split("Build fingerprint: '"))>1 else None
    channel = fingerprint[0] if fingerprint is not None else None
    device_model = fingerprint[1] if fingerprint is not None else None
    device_os_version = fingerprint[2] if fingerprint is not None else None
    pid = get_value("pid: ", ',')
    tid = get_value('tid: ', ',')
    other_threads = get_value('tid: %s, name:' % tid, '\n')
    backtrace = get_value('backtrace:', 'F libc    :')
    java_exception = get_value(' FATAL EXCEPTION: ', ' more\n')
    crash = get_value('// CRASH:', '\n')
    return CRASH(title, time=time, process=procese, ABI=ABI, channel=channel, device_model=device_model,
                 device_os_version=device_os_version, pid=pid, tid=tid, other_threads=other_threads,
                 backtrace=backtrace, java_exception=java_exception, crash_info=crash)


if __name__ == '__main__':
    # print(get_anr_info('/Users/zhuhuiping/Downloads/bugreport-BMH-AN10-HUAWEIBMH-AN10-2021-06-24-21-39-49.zip'))
    print(analyze_anr_info('/Users/zhuhuiping/Downloads/bugreport-BMH-AN10-HUAWEIBMH-AN10-2021-06-24-21-39-49.zip'))
    # print(analyze_crash_info('/Users/zhuhuiping/project/DuLab/cases-library/report/20211021151729_52dc62d9_picture_trend_detail/crash.log'))
    # print(os.listdir('/Users/zhuhuiping/Desktop/脚本/bugreport'))
    # print(get_anr_info('/Users/zhuhuiping/Desktop/脚本/bugreport.zip'))



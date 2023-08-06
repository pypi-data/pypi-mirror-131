import os


def get_android_platform_bridge_list():
    # popen返回文件对象，跟open操作一样
    f = os.popen(r"adb devices", "r")
    out = f.read()
    f.close()
    # 输出结果字符串处理
    new = [x for x in out.split('\n') if x != '']

    # 可能有多个手机设备
    devices = []  # 获取设备名称
    for i in new:
        dev = i.split('\tdevice')
        if len(dev) >= 2:
            devices.append(dev[0])
    return devices


def get_device_build_version(serialno):
    f = os.popen(r"adb -s %s shell getprop ro.build.version.release" % serialno, "r")
    out = f.read()
    f.close()
    # 输出结果字符串处理
    return out.split('\n')[0]


def get_device_product_brand(serialno):
    f = os.popen(r"adb -s %s -d shell getprop ro.product.brand" % serialno, "r")
    out = f.read()
    f.close()
    # 输出结果字符串处理
    return out.split('\n')[0]


def get_device_product_model(serialno):
    f = os.popen(r"adb -s %s -d shell getprop ro.product.model" % serialno, "r")
    out = f.read()
    f.close()
    # 输出结果字符串处理
    return out.split('\n')[0]

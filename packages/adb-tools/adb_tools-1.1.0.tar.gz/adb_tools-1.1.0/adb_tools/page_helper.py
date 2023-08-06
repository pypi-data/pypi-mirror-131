import os
import time

UNRELATED_PAGE = ["SupportRequestManagerFragment"]

def remove_unrelated_page(lst):
    for e in UNRELATED_PAGE:
        for i in lst:
            if i.startswith(e):
                lst.remove(i)
    return lst

def current_page_stack_top(serialno):
    activity = ''
    s = f"adb -s {serialno} shell dumpsys activity top"
    f = os.popen(s, "r")
    adb_info = f.read()
    f.close()
    time.sleep(1)

    adb_info_lines = adb_info.split('\n')
    adb_info_lines = [x for x in adb_info_lines if x != '']

    def get_level(t) -> int:
        for i in range(len(t)):
            if t[i] != ' ':
                return i
        return 0

    stack = []
    ret = []
    contain_app = False
    for line in adb_info_lines:
        level = get_level(line)
        line = line.strip()
        if line.startswith('ACTIVITY') and "com.shizhuang.duapp" in line:
            contain_app = True
            activity = line.split(' ')[1]
        if not contain_app:
            continue
        stack.append((line, level))
        if line.startswith("mState=7"):
            while True:
                pop_item = stack.pop()
                if pop_item[1] < level:
                    if "Active Fragments:" in pop_item[0]:
                        ret.append(pop_item[0].split("Active Fragments:")[1].strip().split('{')[0])
                        break
                    else:
                        ret.append(pop_item[0].split('{')[0])
                        break

    ret = remove_unrelated_page(ret)
    return activity, ret


if __name__=="__main__":
    print(current_page_stack_top('52dc62d9'))
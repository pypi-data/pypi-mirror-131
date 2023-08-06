class CRASH(object):
    def __init__(self, title, app_version=None, time=None, channel=None, device_model=None,
                 device_os_version=None, process=None, pid=None, tid=None, ABI=None,
                 other_threads=None, backtrace=None, java_exception=None, crash_info=None, **kwargs):
        self.title = title
        self.app_version = app_version
        self.channel = channel
        self.time = time
        self.device_model = device_model
        self.device_os_version = device_os_version
        self.process = process
        self.pid = pid
        self.tid = tid
        self.ABI_list = ABI
        self.other_threads = other_threads
        self.backtrace = backtrace
        self.java_exception = java_exception
        self.crash_info = crash_info

    def __str__(self):
        return 'title: %s \nTime: %s \nAPP Version: %s \nDevice Channel: %s \n' \
               'Device Model: %s \nDevice OS Version: %s \n' \
               'Pid: %s \nTid: %s \nABI: %s \n' \
               'Process Name: %s \nOther Threads: %s \nBacktrace: %s \nJava Exception: %s\n' % (
                   self.title,
                   self.time,
                   self.app_version,
                   self.channel,
                   self.device_model,
                   self.device_os_version,
                   self.pid,
                   self.tid,
                   self.ABI_list,
                   self.process,
                   self.other_threads,
                   self.backtrace if self.backtrace is not None else 'Null',
                   self.java_exception if self.java_exception is not None else 'Null' + self.crash_info if self.crash_info is not None else ''
               )

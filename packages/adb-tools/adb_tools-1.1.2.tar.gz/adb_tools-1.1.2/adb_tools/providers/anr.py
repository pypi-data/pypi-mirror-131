class ANR(object):
    def __init__(self, reason=None, time=None, description=None):
        self.reason = reason
        self.time = time

    def __str__(self):
        return 'ANR time: %s \nReason: %s' % (self.time, self.reason)
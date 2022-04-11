from datetime import datetime
class Logger():
    """A logger utility.
    """
    #           0       1        2       3          4
    _levels = ['TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR']
    Level = 2

    @staticmethod
    def parse_level(stringLevel):
        stringLevel = stringLevel.lower()
        stringLevels = [l.lower() for l in Logger._levels]
        if stringLevel in stringLevels:
            return stringLevels.index(stringLevel)
        return None

    @staticmethod
    def _log(level, msg, fields=None):
        t = datetime.now()
        txt = '{} | {: ^7} | "{}"'.format(t.isoformat(), Logger._levels[level], msg)
        if fields is not None:
            txt += ' '
            for k, v in fields.items():
                txt += '{}={} '.format(k, v)
        if Logger.Level <= level:
            print (txt)

    @staticmethod
    def trace(msg, fields=None):
        Logger._log(0, msg, fields=fields)

    @staticmethod
    def debug(msg, fields=None):
        Logger._log(1, msg, fields=fields)

    @staticmethod
    def info(msg, fields=None):
        Logger._log(2, msg, fields=fields)

    @staticmethod
    def warning(msg, fields=None):
        Logger._log(3, msg, fields=fields)

    @staticmethod
    def error(msg, fields=None):
        Logger._log(4, msg, fields=fields)
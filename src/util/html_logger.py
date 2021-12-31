import datetime, multiprocessing, threading, sys, traceback, os
from define import BASE_DIR

class HtmlLogger:
    INFO        = 'INFO'
    HIGHLIGHT   = 'HIGHLIGHT'
    WARNING     = 'WARNING'
    ERROR       = 'ERROR'

    def __init__(self, file_name):
        self._base_dir = BASE_DIR
        self._log_path = os.path.join(self._base_dir, 'var', 'log')
        self._file_name = file_name
        self._yymmdd = self._get_date()
        self._queue = multiprocessing.Queue(-1)
        self._open_file()
        t = threading.Thread(target=self._process)
        t.daemon = True
        t.start()

    def info(self, message):
        self.write(self.INFO, message)

    def highlight(self, message):
        self.write(self.HIGHLIGHT, message)

    def warning(self, message):
        self.write(self.WARNING, message)

    def error(self, message):
        self.write(self.ERROR, message)

    def write(self, level, message):
        log = '<div style="{}">[{}][{}] {}</div>\n'.format(
            self._get_style(level),
            str(datetime.datetime.now()),
            level,
            message
        )
        self._queue.put(log)

    def _write(self, log):
        if self._check_log_rotate():
            self.close()
            self._yymmdd = self._get_date()
            self._open_file()
        self._log_file.write(log)
        self._log_file.flush()

    def _process(self):
        while True:
            try:
                log = self._queue.get()
                self._write(log)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def close(self):
        self._log_file.close()

    def _open_file(self):
        file_path = self.get_file_path()
        mode = 'w+'
        if os.path.isfile(file_path):
            mode = 'a'
        self._log_file = open(file_path, mode=mode, encoding='utf-8')
        # if mode == 'a':
        #     self._log_file.write(
        #         '\n\n<div style="color: black; background-color: white; height: 40px; text-align: center; font-size: 36px;" data-value="restart">RESTART</div>\n\n')
        # else:
        self._log_file.write('<style>body{background-color: black;}</style>\n')

    def _check_log_rotate(self):
        if self._yymmdd != self._get_date():
            return True
        return False

    def _get_date(self):
        return datetime.datetime.now().strftime('%y%m%d')

    def get_file_path(self):
        return os.path.join(self._log_path, '{}/{}_{}.html'.format(self._log_path, self._file_name, self._yymmdd))

    def _get_style(self, level):
        if level == self.INFO:
            return 'color: white; '
        if level == self.HIGHLIGHT:
            return 'color: skyblue; '
        if level == self.WARNING:
            return 'color: orange; '
        if level == self.ERROR:
            return 'color: red; '

import inspect

def get_current_location():
    frame = inspect.currentframe()
    filename = frame.f_code.co_filename  # 当前文件名
    lineno = frame.f_lineno  # 当前行号
    return filename, lineno

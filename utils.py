def bytesFormat(size, precision = 2, step = 1024):
    units = ('B','kB','MB','GB','TB','PB','EB','ZB','YB')
    i = 0

    while (size / step) > 0.9:
        size = size / step
        i += 1
    
    size = round(size, precision)

    return str(size) + units[i]

def calc_speed(start, end, bytes):
    dif = end - start

    if bytes == 0 or dif < 0.01:
        return 0

    return bytes / dif
    
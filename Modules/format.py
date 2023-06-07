def duration(duration):
    hours = int(duration / 3600)
    minutes = int(duration / 60) % 60
    seconds = int(duration % 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def size(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f'{size:.2f} {units[index]}'
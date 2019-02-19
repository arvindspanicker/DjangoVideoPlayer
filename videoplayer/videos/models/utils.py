import os
VIDEO_UPLOAD_PATH = 'videos'

def update_filename(instance, filename):
    extension = get_extension(filename)
    path = VIDEO_UPLOAD_PATH
    format = instance.title + extension
    return os.path.join(path, format)


def get_extension(filename):
    return filename[filename.rfind('.'):]

def format_filename(filename):
    return filename.replace(' ','_')
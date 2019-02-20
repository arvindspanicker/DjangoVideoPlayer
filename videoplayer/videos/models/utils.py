# Python imports
import os

# Constants
VIDEO_UPLOAD_PATH = 'videos'

def update_filename(instance, filename):
    """
    Function that updates the filename - joins the title of the video and the path required.
    :param instance: Video File Instance
    :param filename: filename of the uploaded file
    :return: Full path of the file that needs to be stored
    """
    extension = get_extension(filename)
    path = VIDEO_UPLOAD_PATH
    format = instance.title + extension
    return os.path.join(path, format)


def get_extension(filename):
    """
    Function that gets the extension from the filename
    :param filename: filename of the file
    :return: Extension of the file
    """

    return filename[filename.rfind('.'):]

def format_filename(filename):
    """
    Function that formats the filename - removes spaces
    :param filename: filename as a string
    :return: formatted filename
    """

    return filename.replace(' ','_')
import re

def convert_path_to_windows_format(path):
    """
    Converts the path to a Windows path.
    Converts slashes, directories with spaces in the name.
    Converts Window's prohibited characters to "-".

    Args:
        - path: Can be a Windows or Unix path.
    """
    if "\\" in path and "/" in path:
        # It's Unix format with some space in the name of something.
        wpath = []
        for dir in path.split("/"):
            if "\\" in dir:
                dir = "\"{}\"".format(dir.replace("\\", ""))
            wpath.append(dir)
        path = "\\".join(wpath)
    elif "/":
        # It's Unix format without spaces in the name
        path = path.replace("/", "\\")
    # If not is already windows format
    path = re.sub("[:?<>|]", "-", path)
    return path

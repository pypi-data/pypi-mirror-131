import os
import logging

logger = logging.getLogger("iupy/myconfig")


def get_file_handle_ro(file_name):
    """
    This function returns a read-only file handle for a given name, debug logging exceptions.  Not finding a file
    is not a critical issue for calling this function.

    If the file is opened, the file handle will be returned.  Otherwise, a value of None is returned and the
    resulting exception is logged to DEBUG.

    :param file_name:
    :return:
    """

    logger = logging.getLogger("iupy/myconfig/get_file_handle_ro")

    file_handle = None

    try:
        file_handle = open(file_name, 'r')
    except Exception as error_message:
        logger.debug("{} inaccessible: {}".format(file_name, error_message))

    return file_handle


def get_my_config(cfg_file, **kwargs):
    """
    This function iterates through a series of directories in order to location a configuration file which can
    be used my a larger program.  If found, the contents of the file, the filename, as well as the timestamp of
    the file will be returned as a dictionary.  Otherwise, a value of None is returned.

    It is up to the calling function to determine if this is an error-causing condition.

    :param cfg_file:
    :param kwargs: subdir

    :return:
    """

    logger = logging.getLogger("iupy/myconfig/get_my_config")

    # Look in executing Directory
    # ./configfile

    file_name = cfg_file
    file_handle = get_file_handle_ro(file_name)

    # Look in user's home directory.
    # ~/configfile

    if not file_handle:
        file_name = "{}/{}".format(os.path.expanduser("~"), cfg_file)
        file_handle = get_file_handle_ro(file_name)

    # Check OS for variable IUPY_CFG, and scan that directory set next.

    local_config_dir = os.getenv("IUPY_CFG")

    if local_config_dir:

        # Check base config directory
        # $IUPY_CFG/configfile

        if not file_handle:
            file_name = "{}/{}".format(local_config_dir, cfg_file)
            file_handle = get_file_handle_ro(file_name)

        # Check subdirectory if one is provided.
        # $IUPY_CFG/subdir/configfile

        try:
            if not file_handle and kwargs['subdir']:
                file_name = "{}/{}/{}".format(local_config_dir, kwargs['subdir'], cfg_file)
                file_handle = get_file_handle_ro(file_name)
        except KeyError:
            # Subdirectory not passed.
            pass

    # Look through the POSIX directory structure.  Linux, macOS, FreeBSD, etc.

    if os.name == "posix":

        # /usr/local/etc/configfile

        if not file_handle:
            file_name = "/usr/local/etc/{}".format(cfg_file)
            file_handle = get_file_handle_ro(file_name)

        # /usr/local/etc/subdir/configfile

        try:
            if not file_handle and kwargs['subdir']:
                file_name = "/usr/local/etc/{}/{}".format(kwargs['subdir'], cfg_file)
                file_handle = get_file_handle_ro(file_name)
        except KeyError:
            # Subdirectory keyword not passed.
            pass

        # /etc/configfile

        if not file_handle:
            file_name = "/etc/{}".format(cfg_file)
            file_handle = get_file_handle_ro(file_name)

        # /etc/subdir/configfile

        try:
            if not file_handle and kwargs['subdir']:
                file_name = "/etc/{}/{}".format(kwargs['subdir'], cfg_file)
                file_handle = get_file_handle_ro(file_name)
        except KeyError:
            # Subdirectory keyword not passed.
            pass

    # If there's a file, read and return its contents.

    if file_handle:
        logger.debug("File {} Exists! \n".format(file_name))
        cfg_data = file_handle.read()
        file_handle.close()
        filetime = os.path.getmtime(file_name)

        return {"data": cfg_data, "file": file_name, "filetime": filetime}

    # There are no files.

    logger.debug("File {} could not be loaded.".format(cfg_file))

    return None

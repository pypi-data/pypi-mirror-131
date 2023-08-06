from .helpers import execute_shell
import os

UPDATE_HOSTFILE_SCRIPT_PATH = "/tmp/update_hostfile.sh"


def update_hostfile(logger):
    if os.path.exists(UPDATE_HOSTFILE_SCRIPT_PATH):
        logger.info(f"Found file: {UPDATE_HOSTFILE_SCRIPT_PATH}. Running...")
        stdout_, stderr_, returncode, timed_out = execute_shell(
            f"sh {UPDATE_HOSTFILE_SCRIPT_PATH}", timeout=30, verbose=False
        )
        if returncode == 0:
            logger.info(f"Update Hostfile: SUCCESS")
        else:
            logger.warning(f"Update Hostfile: FAILED")
        logger.debug(f"Update Hostfile returncode: {returncode}")
        logger.debug(f"Update Hostfile timed_out: {timed_out}")
        logger.debug(f"Update Hostfile STDOUT:\n{stdout_}")
        logger.debug(f"Update Hostfile STDERR:\n{stderr_}")
    else:
        logger.warning(
            f"Could not update hostfile. File not found: {UPDATE_HOSTFILE_SCRIPT_PATH}."
        )

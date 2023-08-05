# (c) 2020 Frabit Project maintained and limited by Blylei < blylei.info@gmail.com >
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This file is part of Frabit
#
import errno
import logging
import os
import signal
import time
from glob import glob

from frabit import output
from frabit.exceptions import LockFileParsingError
from frabit.lock import ServerBinlogSyncLock

_logger = logging.getLogger(__name__)


class ProcessInfo:
    """
    frabit process representation
    """

    def __init__(self, pid, server_name, task):
        """
        This object contains all the information required to identify a
        frabit process

        :param int pid: Process ID
        :param string server_name: Name of the server owning the process
        :param string task: Task name (receive-wal, archive-wal...)
        """

        self.pid = pid
        self.server_name = server_name
        self.task = task


class ProcessManager:
    """
    Class for the management of frabit processes owned by a server
    """

    # Map containing the tasks we want to retrieve (and eventually manage)
    TASKS = {
        'receive-wal': ServerBinlogSyncLock
    }

    def __init__(self, config):
        """
        Build a ProcessManager for the provided server

        :param config: configuration of the server owning the process manager
        """
        self.config = config
        self.process_list = []
        # Cycle over the lock files in the lock directory for this server
        for path in glob(os.path.join(self.config.frabit_lock_directory, '.{}-*.lock'.format(self.config.name))):
            for task, lock_class in self.TASKS.items():
                # Check the lock_name against the lock class
                lock = lock_class.build_if_matches(path)
                if lock:
                    try:
                        # Use the lock to get the owner pid
                        pid = lock.get_owner_pid()
                    except LockFileParsingError:
                        _logger.warning(
                            "Skipping the {task} process for server {name}: "
                            "Error reading the PID from lock file '{path}'".format(
                                task=task, name=self.config.name, path=path)
                            )

                        break
                    # If there is a pid save it in the process list
                    if pid:
                        self.process_list.append(ProcessInfo(pid, config.name, task))
                    # In any case, we found a match, so we must stop iterating
                    # over the task types and handle the the next path
                    break

    def list(self, task_filter=None):
        """
        Returns a list of processes owned by this server

        If no filter is provided, all the processes are returned.

        :param str task_filter: Type of process we want to retrieve
        :return list[ProcessInfo]: List of processes for the server
        """
        server_tasks = []
        for process in self.process_list:
            # Filter the processes if necessary
            if task_filter and process.task != task_filter:
                continue
            server_tasks.append(process)
        return server_tasks

    def kill(self, process_info, retries=10):
        """
        Kill a process

        Returns True if killed successfully False otherwise

        :param ProcessInfo process_info: representation of the process
            we want to kill
        :param int retries: number of times the method will check
            if the process is still alive
        :rtype: bool
        """
        # Try to kill the process
        try:
            _logger.debug("Sending SIGINT to PID {}".format(process_info.pid))
            os.kill(process_info.pid, signal.SIGINT)
            _logger.debug("os.kill call succeeded")
        except OSError as e:
            _logger.debug("os.kill call failed: {}".format(e))
            # The process doesn't exists. It has probably just terminated.
            if e.errno == errno.ESRCH:
                return True
            # Something unexpected has happened
            output.error("{}".format(e))
            return False
        # Check if the process have been killed. the fastest (and maybe safest)
        # way is to send a kill with 0 as signal.
        # If the method returns an OSError exceptions, the process have been
        # killed successfully, otherwise is still alive.
        for counter in range(retries):
            try:
                _logger.debug("Checking with SIG_DFL if PID {} is still alive".format(process_info.pid))
                os.kill(process_info.pid, signal.SIG_DFL)
                _logger.debug("os.kill call succeeded")
            except OSError as e:
                _logger.debug("os.kill call failed: {}".format(e))
                # If the process doesn't exists, we are done.
                if e.errno == errno.ESRCH:
                    return True
                # Something unexpected has happened
                output.error("{}".format(e))
                return False
            time.sleep(1)
        _logger.debug("The PID {pid} has not been terminated after {retries} retries".format(pid=process_info.pid,
                                                                                             retries=retries))
        return False

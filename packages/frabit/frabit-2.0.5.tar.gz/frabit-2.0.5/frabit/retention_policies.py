# (c) 2020 Frabit Project maintained and limited by Blylei < blylei.info@gmail.com >
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This file is part of Frabit
#
"""
This module defines backup retention policies. A backup retention
policy in Frabit is a user-defined policy for determining how long
backups and archived logs (binlog files) need to be retained for media
recovery.
You can define a retention policy in terms of backup redundancy
or a recovery window.
Frabit retains the periodical backups required to satisfy the current retention policy,
and any archived binlog files required for complete recovery of those backups.
"""

import logging
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

from dateutil import tz

from frabit.info import BackupInfo
from frabit.utils import with_metaclass

_logger = logging.getLogger(__name__)


class RetentionPolicy(with_metaclass(ABCMeta, object)):
    """Abstract base class for retention policies"""

    def __init__(self, mode, unit, value, context, server):
        """Constructor of the retention policy base class"""
        self.mode = mode
        self.unit = unit
        self.value = int(value)
        self.context = context
        self.server = server
        self._first_backup = None
        self._first_binlog = None

    def report(self, source=None, context=None):
        """Report obsolete/valid objects according to the retention policy"""
        if context is None:
            context = self.context
        # Overrides the list of available backups
        if source is None:
            source = self.server.get_available_backups(BackupInfo.STATUS_NOT_EMPTY)
        if context == 'BASE':
            return self._backup_report(source)
        elif context == 'WAL':
            return self._binlog_report()
        else:
            raise ValueError('Invalid context {}'.format(context))

    def backup_status(self, backup_id):
        """Report the status of a backup according to the retention policy"""
        source = self.server.get_available_backups(BackupInfo.STATUS_NOT_EMPTY)
        if self.context == 'BASE':
            return self._backup_report(source)[backup_id]
        else:
            return BackupInfo.NONE

    def first_backup(self):
        """Returns the first valid backup according to retention policies"""
        if not self._first_backup:
            self.report(context='BASE')
        return self._first_backup

    def first_binlog(self):
        """Returns the first valid BIN according to retention policies"""
        if not self._first_binlog:
            self.report(context='BIN')
        return self._first_binlog

    @abstractmethod
    def __str__(self):
        """String representation"""
        pass

    @abstractmethod
    def debug(self):
        """Debug information"""
        pass

    @abstractmethod
    def _backup_report(self, source):
        """Report obsolete/valid backups according to the retention policy"""
        pass

    @abstractmethod
    def _binlog_report(self):
        """Report obsolete/valid WALs according to the retention policy"""
        pass

    @classmethod
    def create(cls, server, option, value):
        """
        If given option and value from the configuration file match,
        creates the retention policy object for the given server
        """
        # using @abstractclassmethod from python3 would be better here
        raise NotImplementedError(
            'The class {} must override the create() class method'.format(cls.__name__))

    def to_json(self):
        """
        Output representation of the obj for JSON serialization
        """
        return "{mode} {value} {unit}".format(mode=self.mode, value=self.value, unit=self.unit)


class RedundancyRetentionPolicy(RetentionPolicy):
    """
    Retention policy based on redundancy, the setting that determines
    many periodical backups to keep. A redundancy-based retention policy
    is contrasted with retention policy that uses a recovery window.
    """

    _re = re.compile(r'^\s*redundancy\s+(\d+)\s*$', re.IGNORECASE)

    def __init__(self, context, value, server):
        super(RedundancyRetentionPolicy, self).__init__('redundancy', 'b', value, 'BASE', server)
        assert (value >= 0)

    def __str__(self):
        return "REDUNDANCY {}".format(self.value)

    def debug(self):
        return "Redundancy: {value} ({context})".format(value=self.value, context=self.context)

    def _backup_report(self, source):
        """Report obsolete/valid backups according to the retention policy"""
        report = dict()
        backups = source
        # Normalise the redundancy value (according to minimum redundancy)
        redundancy = self.value
        if redundancy < self.server.config.minimum_redundancy:
            _logger.warning(
                "Retention policy redundancy ({redu}) is lower than "
                "the required minimum redundancy ({mini_redu1}). Enforce {mini_redu2}.".format(
                redu=redundancy, mini_redu1=self.server.config.minimum_redundancy,
                mini_redu2=self.server.config.minimum_redundancy)
            )
            redundancy = self.server.config.minimum_redundancy

        # Map the latest 'redundancy' DONE backups as VALID
        # The remaining DONE backups are classified as OBSOLETE
        # Non DONE backups are classified as NONE
        # NOTE: reverse key orders (simulate reverse chronology)
        i = 0
        for bid in sorted(backups.keys(), reverse=True):
            if backups[bid].status == BackupInfo.DONE:
                if i < redundancy:
                    report[bid] = BackupInfo.VALID
                    self._first_backup = bid
                else:
                    report[bid] = BackupInfo.OBSOLETE
                i = i + 1
            else:
                report[bid] = BackupInfo.NONE
        return report

    def _binlog_report(self):
        """Report obsolete/valid binlog files according to the retention policy"""
        pass

    @classmethod
    def create(cls, server, context, optval):
        # Detect Redundancy retention type
        mtch = cls._re.match(optval)
        if not mtch:
            return None
        value = int(mtch.groups()[0])
        return cls(context, value, server)


class RecoveryWindowRetentionPolicy(RetentionPolicy):
    """
    Retention policy based on recovery window. The DBA specifies a period of
    time and Frabit ensures retention of backups and archived binlog files
    required for point-in-time recovery to any time during the recovery window.
    The interval always ends with the current time and extends back in time
    for the number of days specified by the user.
    For example, if the retention policy is set for a recovery window of
    seven days, and the current time is 9:30 AM on Friday, Frabit retains
    the backups required to allow point-in-time recovery back to 9:30 AM
    on the previous Friday.
    """

    _re = re.compile(
        r"""
        ^\s*
        recovery\s+window\s+of\s+   # recovery window of
        (\d+)\s+(day|month|week)s?  # N (day|month|week) with optional 's'
        \s*$
        """,
        re.IGNORECASE | re.VERBOSE)
    _kw = {'d': 'DAYS', 'm': 'MONTHS', 'w': 'WEEKS'}

    def __init__(self, context, value, unit, server):
        super(RecoveryWindowRetentionPolicy, self
              ).__init__('window', unit, value, context, server)
        assert (value >= 0)
        assert (unit == 'd' or unit == 'm' or unit == 'w')
        assert (context == 'WAL' or context == 'BASE')
        # Calculates the time delta
        if unit == 'd':
            self.timedelta = timedelta(days=self.value)
        elif unit == 'w':
            self.timedelta = timedelta(weeks=self.value)
        elif unit == 'm':
            self.timedelta = timedelta(days=(31 * self.value))

    def __str__(self):
        return "RECOVERY WINDOW OF {value} {unit}".format(value=self.value, unit=self._kw[self.unit])

    def debug(self):
        return "Recovery Window: {value} {unit}: {context} ({pirt})".format(
            value=self.value, unit=self.unit, context=self.context,
            pirt=self._point_of_recoverability())

    def _point_of_recoverability(self):
        """
        Based on the current time and the window, calculate the point
        of recoverability, which will be then used to define the first
        backup or the first WAL
        """
        return datetime.now(tz.tzlocal()) - self.timedelta

    def _backup_report(self, source):
        """Report obsolete/valid backups according to the retention policy"""
        report = dict()
        backups = source
        # Map as VALID all DONE backups having end time lower than
        # the point of recoverability. The older ones
        # are classified as OBSOLETE.
        # Non DONE backups are classified as NONE
        found = False
        valid = 0
        # NOTE: reverse key orders (simulate reverse chronology)
        for bid in sorted(backups.keys(), reverse=True):
            # We are interested in DONE backups only
            if backups[bid].status == BackupInfo.DONE:
                if found:
                    # Check minimum redundancy requirements
                    if valid < self.server.config.minimum_redundancy:
                        _logger.warning(
                            "Keeping obsolete backup %s for server %s "
                            "(older than %s) "
                            "due to minimum redundancy requirements (%s)",
                            bid, self.server.config.name,
                            self._point_of_recoverability(),
                            self.server.config.minimum_redundancy)
                        # We mark the backup as potentially obsolete
                        # as we must respect minimum redundancy requirements
                        report[bid] = BackupInfo.POTENTIALLY_OBSOLETE
                        self._first_backup = bid
                        valid = valid + 1
                    else:
                        # We mark this backup as obsolete
                        # (older than the first valid one)
                        _logger.info(
                            "Reporting backup %s for server %s as OBSOLETE "
                            "(older than %s)",
                            bid, self.server.config.name,
                            self._point_of_recoverability())
                        report[bid] = BackupInfo.OBSOLETE
                else:
                    _logger.debug(
                        "Reporting backup %s for server %s as VALID "
                        "(newer than %s)",
                        bid, self.server.config.name,
                        self._point_of_recoverability())
                    # Backup within the recovery window
                    report[bid] = BackupInfo.VALID
                    self._first_backup = bid
                    valid = valid + 1
                    # TODO: Currently we use the backup local end time
                    # We need to make this more accurate
                    if backups[bid].end_time < self._point_of_recoverability():
                        found = True
            else:
                report[bid] = BackupInfo.NONE
        return report

    def _binlog_report(self):
        """Report obsolete/valid WALs according to the retention policy"""
        pass

    @classmethod
    def create(cls, server, context, optval):
        # Detect Recovery Window retention type
        match = cls._re.match(optval)
        if not match:
            return None
        value = int(match.groups()[0])
        unit = match.groups()[1][0].lower()
        return cls(context, value, unit, server)


class SimpleBinlogRetentionPolicy(RetentionPolicy):
    """Simple retention policy for binlog files (identical to the main one)"""
    _re = re.compile(r'^\s*main\s*$', re.IGNORECASE)

    def __init__(self, context, policy, server):
        super(SimpleBinlogRetentionPolicy, self
              ).__init__('simple-binlog', policy.unit, policy.value,
                         context, server)
        # The referred policy must be of type 'BASE'
        assert (self.context == 'WAL' and policy.context == 'BASE')
        self.policy = policy

    def __str__(self):
        return "MAIN"

    def debug(self):
        return "Simple binlog Retention Policy ({policy})".format(self.policy)

    def _backup_report(self, source):
        """Report obsolete/valid backups according to the retention policy"""
        pass

    def _binlog_report(self):
        """Report obsolete/valid backups according to the retention policy"""
        self.policy.report(context='binlog')

    def first_binlog(self):
        """Returns the first valid binlog according to retention policies"""
        return self.policy.first_binlog()

    @classmethod
    def create(cls, server, context, optval):
        # Detect Redundancy retention type
        match = cls._re.match(optval)
        if not match:
            return None
        return cls(context, server.config.retention_policy, server)


class RetentionPolicyFactory(object):
    """Factory for retention policy objects"""

    # Available retention policy types
    policy_classes = [
        RedundancyRetentionPolicy,
        RecoveryWindowRetentionPolicy,
        SimpleBinlogRetentionPolicy
    ]

    @classmethod
    def create(cls, server, option, value):
        """
        Based on the given option and value from the configuration
        file, creates the appropriate retention policy object
        for the given server
        """
        if option == 'wal_retention_policy':
            context = 'BIN'
        elif option == 'retention_policy':
            context = 'BASE'
        else:
            raise ValueError('Unknown option for retention policy: {}'.format(option))

        # Look for the matching rule
        for policy_class in cls.policy_classes:
            policy = policy_class.create(server, context, value)
            if policy:
                return policy

        raise ValueError('Cannot parse option {opt}: {val}'.format(opt=option, val=value))

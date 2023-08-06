"""
Simple recurring job scheduling.

github.com/manorom/recurring_sched

A interface to schedule periodic jobs with python's `sched` module, using a builder
patter for configuration inspired by `schedule` (github.com/dbader/schedule).

Usage:
    >>> from recurring_sched import RecurringScheduler
    >>> def job(message='General Kenobi'):
    >>>     print("Hello There: ", message)
    >>> schedule.every(10).minutes.do(job)
    >>> schedule.every(1).hours.do(job, messages="General Skywalker")
    >>> schedule.run()

"""

import sched
import functools
from datetime import datetime, timedelta

__all__ = ("RecurringScheduler",)


class RecurringJob:
    def __init__(self, interval, rsched):
        self.interval = interval
        self.unit = None
        self._rsched = rsched
        self._at_time = None
        self._prev_run = None
        self._next_run = None
        self._job_func = None

    @property
    def seconds(self):
        """Sets the interval unit of this job to seconds"""
        self.unit = "seconds"
        return self

    @property
    def minutes(self):
        """Sets the interval unit of this job to minutes"""

        self.unit = "minutes"
        return self

    @property
    def hours(self):
        """Sets the interval unit of this job to hours"""

        self.unit = "hours"
        return self

    @property
    def days(self):
        """Sets the interval unit of this job to days"""
        self.unit = "days"
        return self

    def at(self, datetimestr):
        if self.unit not in ("days", "hours", "minutes"):
            raise ValueError("Time unit not set for job")
        if self.unit == "seconds":
            raise ValueError("at() not supported for 'seconds' time unit")
        elif self.unit == "minutes":
            self._at_time = datetime.strptime(datetimestr, "%S")
        elif self.unit == "hours":
            self._at_time = datetime.strptime(datetimestr, "%M:%S")
        elif self.unit == "days":
            self._at_time = datetime.strptime(datetimestr, "%H:%M:%S")

    def _calc_next_abstime(self):
        if self.unit is None:
            raise ValueError(
                "A unit must be set to run a scheduler (using every(n).seconds, "
                "every(n).minutes, every(n).hours, etc"
            )
        elif self.unit == "seconds":
            return self._prev_run + timedelta(seconds=self.interval)
        elif self.unit == "minutes":
            next_run = self._prev_run + timedelta(minutes=self.interval)
            if self._at_time:
                next_run.second = self._at_time.second
            return next_run
        elif self.unit == "hours":
            next_run = self._prev_run + timedelta(hours=self.interval)
            if self._at_time:
                next_run.second = self._at_time.second
                next_run.minute = self._at_time.minute
            return next_run
        elif self.unit == "days":
            next_run = self._prev_run + timedelta(days=self.interval)
            if self._at_time:
                next_run.second = self._at_time.second
                next_run.minute = self._at_time.minute
                next_run.hour = self._at_time.hour
            return next_run

    def _schedule_next_run(self):
        self._prev_run = self._next_run
        if not self._prev_run:
            self._prev_run = datetime.now()
        self._next_run = self._calc_next_abstime()
        ev = self._rsched._sched.enterabs(self._next_run.timestamp(), 0, self._run)

    def _run(self):
        if not self._job_func:
            raise ValueError("Job function not set with .do(func): Cannot run job.")
        self._schedule_next_run()
        self._job_func()

    def do(self, job_func, *args, **kwargs):
        """
        Specifies the function to executed every time this job runs.

        Any additional arguments are passed on to job_func when
        the job runs.

        :param job_func: The callable to be scheduled
        """
        self._job_func = functools.partial(job_func, *args, **kwargs)
        functools.update_wrapper(self._job_func, job_func)
        self._rsched._jobs.append(self)


class RecurringScheduler:
    """
    Holds a :class:`scheduler <sched.scheduler>` instance and can be used to add
    recurring jobs to it, using the :meth:`every <RecurringScheduler.every>`
    builder method.
    """

    def __init__(self, *args, **kwargs):
        self._sched = sched.scheduler(*args, **kwargs)
        self._jobs = []

    def every(self, interval=1):
        """
        Schedule a new recurring job.

        This creates a (unconfigured) job object which can then be used to
        specify interval unit, time of execution and the job to be run.


        :param interval: A quantity of a certain time unit
        :return: An unconfigured :class:`RecurringJobs <RecurringJob>`
        """
        return RecurringJob(interval, self)

    def run(self, *args, **kwargs):
        """
        Runs the :class:`sched.scheduler` instance with all jobs added to the
        :meth:`RecurringScheduler` instance.

        Any additional arguments are passed to :meth:`scheduler.run`.
        """
        for job in self._jobs:
            job._schedule_next_run()
        self._sched.run(*args, **kwargs)

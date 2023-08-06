
import multiprocessing

import pandas as pd

from redengine.core import Scheduler
from redengine.tasks import FuncTask
from redengine.time import TimeDelta
from redengine.conditions import SchedulerStarted, TaskStarted, AlwaysTrue

def run_succeeding():
    pass

def run_creating_child():

    proc = multiprocessing.Process(target=run_succeeding, daemon=True)
    proc.start()

def test_creating_child(tmpdir, session):
    with tmpdir.as_cwd() as old_dir:

        # To be confident the scheduler won't lie to us
        # we test the task execution with a job that has
        # actual measurable impact outside redengine
        FuncTask(run_creating_child, name="task_1", start_cond=AlwaysTrue())
        scheduler = Scheduler(
            shut_cond=(TaskStarted(task="task_1") >= 1) | ~SchedulerStarted(period=TimeDelta("1 second")),
            tasks_as_daemon=False
        )

        scheduler()

        history = pd.DataFrame(session.get_task("task_1").logger.get_records())
        assert 1 == (history["action"] == "run").sum()
        assert 1 == (history["action"] == "success").sum()
        assert 0 == (history["action"] == "fail").sum()

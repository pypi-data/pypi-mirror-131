
import pytest

from redengine.tasks.maintain import Restart
from redengine.tasks import FuncTask
from redengine.core.exceptions import SchedulerRestart
from redengine.core import Scheduler
from redengine.conditions import TaskStarted



def write_file(text):
    with open("test.txt", "a") as f:
        f.write(text)

def test_restart_raises(session):
    task = Restart()
    with pytest.raises(SchedulerRestart):
        task()

def test_scheduler_restart(tmpdir, session):

    with tmpdir.as_cwd() as old_dir:
        
        FuncTask(write_file, parameters={"text": "Started"}, on_startup=True, name="startup", execution="main")
        FuncTask(write_file, parameters={"text": "Shut"}, on_shutdown=True, name="shutdown", execution="main")

        task = Restart()

        task.force_run = True
        
        scheduler = Scheduler(
            shut_cond=TaskStarted(task=task) == 1,
            restarting="recall"
        )
        scheduler()

        with open("test.txt") as f:
            cont = f.read()
        assert "StartedShutStartedShut" == cont

        history = list(task.logger.get_records())
        assert 1 == len([record for record in history if record["action"] == "run"])
        assert 1 == len([record for record in history if record["action"] == "success"])

# TODO: Test 
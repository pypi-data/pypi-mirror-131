
import pytest
from redengine.conditions import TaskCond
from redengine.conditions import SchedulerCycles, SchedulerStarted, TaskStarted, AlwaysFalse, AlwaysTrue
import re

from redengine.core import Scheduler
from redengine.tasks import FuncTask

def is_foo(status):
    print(f"evaluating: {status}")
    if status == "true":
        return True
    else:
        return False

@pytest.mark.parametrize("execution", ["main", "thread", "process"])
def test_taskcond_true(capsys, session, execution):

    cond = TaskCond(syntax=re.compile(r"is foo (?P<status>.+)"), start_cond="every 1 min", active_time="past 10 seconds", execution=execution)
    cond(is_foo)
    
    task = FuncTask(lambda: None, start_cond="is foo true", name="a task", execution="main")

    scheduler = Scheduler( # (TaskStarted(task="a task") >= 2) | 
        shut_cond=(TaskStarted(task="a task") >= 2) | ~SchedulerStarted(period="past 5 seconds")
    )

    scheduler()
    
    history = list(session.get_task_log())
    history_task = [
        {"task_name": rec['task_name'], "action": rec["action"]} 
        for rec in history
        if rec['task_name'] == "a task"
    ]
    assert history_task == [
        {"task_name": "a task", "action": "run"},
        {"task_name": "a task", "action": "success"},
        {"task_name": "a task", "action": "run"},
        {"task_name": "a task", "action": "success"},
    ]

    # Check cond task
    cond_tasks = [task for task in session.tasks.values() if task.name.startswith("_condition")]
    assert len(cond_tasks) == 1

    cond_task = cond_tasks[0]
    history_check = [
        {"task_name": rec['task_name'], "action": rec["action"]} 
        for rec in history
        if rec['task_name'] == cond_task.name
    ]
    assert history_check == [
        {"task_name": cond_task.name, "action": "run"},
        {"task_name": cond_task.name, "action": "success"},
    ] 

@pytest.mark.parametrize("execution", ["main", "thread", "process"])
def test_taskcond_false(capsys, session, execution):

    cond = TaskCond(syntax=re.compile(r"is foo (?P<status>.+)"), start_cond="every 1 min", active_time="past 10 seconds", execution=execution)
    cond(is_foo)
    
    task = FuncTask(lambda: None, start_cond="is foo false", name="a task", execution="main")

    scheduler = Scheduler( # (TaskStarted(task="a task") >= 2) | 
        shut_cond=SchedulerCycles() >= 3
    )

    scheduler()
    
    history = list(session.get_task_log())
    history_task = [
        {"task_name": rec['task_name'], "action": rec["action"]} 
        for rec in history
        if rec['task_name'] == "a task"
    ]
    assert history_task == []

    # Check cond task
    cond_tasks = [task for task in session.tasks.values() if task.name.startswith("_condition")]
    assert len(cond_tasks) == 1
    
    cond_task = cond_tasks[0]
    history_check = [
        {"task_name": rec['task_name'], "action": rec["action"]} 
        for rec in history
        if rec['task_name'] == cond_task.name
    ]
    assert history_check == [
        {"task_name": cond_task.name, "action": "run"},
        {"task_name": cond_task.name, "action": "success"},
    ] 


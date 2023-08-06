
from redengine.extensions import Sequence
from redengine.extensions.piping import TriggerCluster
from redengine.conditions import All
from redengine import Session

def test_parse():
    conf = {
        "tasks": {
            "mytask-1": {"class": "FuncTask", "path": "path/to/first.py", "func": "main"},
            "mytask-2": {"class": "FuncTask", "path": "path/to/second.py", "func": "main", "start_cond": "daily"},
            "mytask-3": {"class": "FuncTask", "path": "path/to/second.py", "func": "main", "start_cond": "daily"},
        },
        "sequences": {
            "my-sequence-1": {
                "tasks": ["mytask-1", "mytask-2"],
            },
            "my-sequence-2": {
                "tasks": ["mytask-2", "mytask-3"],
            }
        }
    }

    #assert {} == session.extensions
    session = Session.from_dict(conf)
    sequences = session.extensions["sequences"]
    assert isinstance(sequences["my-sequence-1"], Sequence)
    assert isinstance(sequences["my-sequence-2"], Sequence)
    assert "Sequence(tasks=['mytask-1', 'mytask-2'], interval=None)" == repr(sequences["my-sequence-1"])
    
    # Test conditions
    task1 = session.tasks["mytask-1"]
    task2 = session.tasks["mytask-2"]
    task3 = session.tasks["mytask-3"]
    assert isinstance(task1.start_cond, TriggerCluster)
    assert isinstance(task2.start_cond, All)
    assert isinstance(task2.start_cond[1], TriggerCluster)
    assert isinstance(task3.start_cond[1], TriggerCluster)

    # Test sequences
    assert sequences["my-sequence-1"].triggers[0].task is task1
    assert sequences["my-sequence-1"].triggers[1].task is task2

    assert sequences["my-sequence-2"].triggers[0].task is task2
    assert sequences["my-sequence-2"].triggers[1].task is task3

    # test Sequence Triggers
    task1_trigger = task1.start_cond[0]
    # assert task1_trigger.depend_trigger is None
    assert task1_trigger.task is task1

    task2_seq1_trigger = task2.start_cond[1][0]
    # assert task2_seq1_trigger.depend_trigger is task1_trigger
    assert task2_seq1_trigger.task is task2

    task2_seq2_trigger = task2.start_cond[1][1]
    # assert task2_seq2_trigger.depend_trigger is None
    assert task2_seq2_trigger.task is task2

    task3_seq2_trigger = task3.start_cond[1][0]
    # assert task3_seq2_trigger.depend_trigger is task2_seq2_trigger
    assert task3_seq2_trigger.task is task3

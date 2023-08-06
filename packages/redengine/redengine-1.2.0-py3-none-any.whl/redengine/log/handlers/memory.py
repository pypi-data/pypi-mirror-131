
import logging
from logging import Handler
from typing import List, Dict
from copy import copy


class MemoryHandler(Handler):
    """A handler class which stores the log records
    to an in-memory list.

    Parameters
    ----------
    store_as : str, {'dict', 'record'}
        How the records are stored. If 'record',
        the records are kept as LogRecord objects.


    Examples
    --------

    >>> from redengine.log import MemoryHandler
    >>> handler = MemoryHandler(store_as="dict") # doctest: +SKIP
    """

    def __init__(self, store_as="record", **kwargs):
        super().__init__(**kwargs)
        self.records = []
        self.store_as = store_as
        
    def emit(self, record:logging.LogRecord):
        record = copy(record)
        msg = self.format(record)
        if isinstance(msg, (dict, logging.LogRecord)):
            record = msg
        else:
            record.formatted_message = msg

        if self.store_as == "record":
            self.records.append(record)
        elif self.store_as == "dict":
            self.records.append(vars(record))
        else:
            raise ValueError(f"Invalid value: {self.store_as}")

# Extras
    def read(self, **kwargs) -> List[Dict]:
        "Read the logs"
        yield from self.records
        
    def clear_log(self):
        "Empty the logging storage"
        self.records = []
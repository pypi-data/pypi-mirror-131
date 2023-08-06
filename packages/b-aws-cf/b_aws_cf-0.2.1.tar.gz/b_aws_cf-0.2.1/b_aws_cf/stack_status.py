from enum import Enum, auto
from typing import List


class StackStatus(Enum):
    CREATE_IN_PROGRESS = auto()
    CREATE_FAILED = auto()
    CREATE_COMPLETE = auto()
    ROLLBACK_IN_PROGRESS = auto()
    ROLLBACK_FAILED = auto()
    ROLLBACK_COMPLETE = auto()
    DELETE_IN_PROGRESS = auto()
    DELETE_FAILED = auto()
    DELETE_COMPLETE = auto()
    UPDATE_IN_PROGRESS = auto()
    UPDATE_COMPLETE_CLEANUP_IN_PROGRESS = auto()
    UPDATE_COMPLETE = auto()
    UPDATE_FAILED = auto()
    UPDATE_ROLLBACK_IN_PROGRESS = auto()
    UPDATE_ROLLBACK_FAILED = auto()
    UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS = auto()
    UPDATE_ROLLBACK_COMPLETE = auto()
    REVIEW_IN_PROGRESS = auto()
    IMPORT_IN_PROGRESS = auto()
    IMPORT_COMPLETE = auto()
    IMPORT_ROLLBACK_IN_PROGRESS = auto()
    IMPORT_ROLLBACK_FAILED = auto()
    IMPORT_ROLLBACK_COMPLETE = auto()

    @staticmethod
    def to_list() -> List['StackStatus']:
        items = []
        for i in StackStatus:
            items.append(i)
        return items

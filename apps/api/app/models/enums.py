from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    AGENT = "agent"
    OPERATOR = "operator"


class ComplaintStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CANCELED = "canceled"


class MissionStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class DatasetSplit(str, Enum):
    TRAIN = "train"
    VALID = "valid"
    TEST = "test"


class ModelTask(str, Enum):
    OBJECT_DETECTION = "object_detection"


class RiskLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"

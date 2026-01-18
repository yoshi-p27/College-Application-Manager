# Re-export models from core app for submission requirements
# The actual models are in core/models.py for proper Django app structure
from core.models import (
    District,
    HighSchool,
    Student,
    College,
    Application,
    Course,
    Enrollment,
)

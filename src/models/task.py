from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
import uuid


class Task(BaseModel):
    """
    Represents a single todo item with properties:
    unique ID, title (required), description (optional),
    completion status (boolean), creation timestamp
    """
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or contain only whitespace')
        if len(v) > 200:
            raise ValueError('Title must be 200 characters or less')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v

    def __init__(self, **data):
        # Generate ID if not provided
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())

        # Set timestamps if not provided
        now = datetime.now()
        if 'created_at' not in data or not data['created_at']:
            data['created_at'] = now
        if 'updated_at' not in data or not data['updated_at']:
            data['updated_at'] = now

        super().__init__(**data)

    def mark_complete(self):
        """Mark the task as complete and update the timestamp"""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self):
        """Mark the task as incomplete and update the timestamp"""
        self.completed = False
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None):
        """Update task fields and update the timestamp"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()
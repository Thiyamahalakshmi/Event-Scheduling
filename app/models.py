from .extensions import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)

    allocations = db.relationship('EventResourceAllocation', back_populates='event', cascade='all, delete-orphan')

    def duration_hours(self):
        return (self.end_time - self.start_time).total_seconds() / 3600.0

class Resource(db.Model):
    __tablename__ = 'resource'
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(80))
    capacity = db.Column(db.Integer, default=1)

    allocations = db.relationship('EventResourceAllocation', back_populates='resource', cascade='all, delete-orphan')

class EventResourceAllocation(db.Model):
    __tablename__ = 'event_resource_allocation'
    allocation_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.resource_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    event = db.relationship('Event', back_populates='allocations')
    resource = db.relationship('Resource', back_populates='allocations')

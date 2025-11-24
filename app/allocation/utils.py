from ..models import EventResourceAllocation, Event, Resource
from ..extensions import db

def events_overlap(a_start, a_end, b_start, b_end):
    return (a_start < b_end) and (b_start < a_end)

def check_conflict_for_allocation(event, resource, qty=1):
    overlaps = db.session.query(EventResourceAllocation).join(Event).filter(
        EventResourceAllocation.resource_id == resource.resource_id
    ).all()
    total = qty
    for a in overlaps:
        if events_overlap(event.start_time, event.end_time, a.event.start_time, a.event.end_time):
            total += a.quantity
    if total > resource.capacity:
        return f"Resource '{resource.resource_name}' capacity exceeded: required {total}, capacity {resource.capacity}"
    return None

def check_conflicts_for_event(event):
    conf_msgs = []
    for a in event.allocations:
        resource = a.resource
        others = db.session.query(EventResourceAllocation).join(Event).filter(
            EventResourceAllocation.resource_id == resource.resource_id,
            EventResourceAllocation.allocation_id != a.allocation_id
        ).all()
        total = a.quantity
        for o in others:
            if events_overlap(event.start_time, event.end_time, o.event.start_time, o.event.end_time):
                total += o.quantity
        if total > resource.capacity:
            conf_msgs.append(f"Resource {resource.resource_name} would be overallocated (need {total}, cap {resource.capacity})")
    return conf_msgs

from flask import Blueprint, jsonify, request
from ..models import Event, Resource, EventResourceAllocation
bp = Blueprint('api', __name__)

@bp.route('/events')
def events():
    evs = Event.query.order_by(Event.start_time).all()
    return jsonify([{'event_id':e.event_id,'title':e.title,'start_time':e.start_time.isoformat(),'end_time':e.end_time.isoformat()} for e in evs])

@bp.route('/resources')
def resources():
    rs = Resource.query.all()
    return jsonify([{'resource_id':r.resource_id,'name':r.resource_name,'type':r.resource_type,'capacity':r.capacity} for r in rs])

@bp.route('/allocations')
def allocations():
    allocs = EventResourceAllocation.query.all()
    return jsonify([{'allocation_id':a.allocation_id,'event_id':a.event_id,'resource_id':a.resource_id,'quantity':a.quantity} for a in allocs])

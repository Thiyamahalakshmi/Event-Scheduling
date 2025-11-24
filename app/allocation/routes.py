from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models import Event, Resource, EventResourceAllocation
from ..allocation.forms import AllocationForm
from ..allocation.utils import check_conflict_for_allocation

bp = Blueprint('allocation', __name__, template_folder='templates')

@bp.route('/')
def list_allocations():
    allocs = EventResourceAllocation.query.order_by(EventResourceAllocation.allocation_id.desc()).all()
    return render_template('allocation/list.html', allocations=allocs)

@bp.route('/create', methods=['GET','POST'])
def create_allocation():
    form = AllocationForm()
    form.event_id.choices = [(e.event_id, f"{e.title} ({e.start_time.strftime('%Y-%m-%d %H:%M')})") for e in Event.query.order_by(Event.start_time).all()]
    form.resource_id.choices = [(r.resource_id, r.resource_name) for r in Resource.query.order_by(Resource.resource_name).all()]
    if form.validate_on_submit():
        event = Event.query.get(form.event_id.data)
        resource = Resource.query.get(form.resource_id.data)
        qty = form.quantity.data or 1
        conflict_msg = check_conflict_for_allocation(event, resource, qty)
        if conflict_msg:
            flash('Conflict: ' + conflict_msg, 'danger')
            return redirect(url_for('allocation.create_allocation'))
        alloc = EventResourceAllocation(event_id=event.event_id, resource_id=resource.resource_id, quantity=qty)
        db.session.add(alloc)
        db.session.commit()
        flash('Resource allocated', 'success')
        return redirect(url_for('allocation.list_allocations'))
    return render_template('allocation/create.html', form=form)

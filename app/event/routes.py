from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models import Event, Resource, EventResourceAllocation
from ..event.forms import EventForm
from ..allocation.utils import check_conflicts_for_event

bp = Blueprint('event', __name__, template_folder='templates')

@bp.route('/')
def list_events():
    events = Event.query.order_by(Event.start_time).all()
    return render_template('event/list.html', events=events)

@bp.route('/create', methods=['GET','POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        ev = Event(title=form.title.data, start_time=form.start_time.data, end_time=form.end_time.data, description=form.description.data)
        if ev.end_time <= ev.start_time:
            flash('End time must be after start time', 'danger')
            return render_template('event/create.html', form=form)
        db.session.add(ev)
        db.session.commit()
        flash('Event created', 'success')
        return redirect(url_for('event.list_events'))
    return render_template('event/create.html', form=form)

@bp.route('/<int:event_id>/edit', methods=['GET','POST'])
def edit_event(event_id):
    ev = Event.query.get_or_404(event_id)
    form = EventForm(obj=ev)
    if form.validate_on_submit():
        ev.title = form.title.data
        ev.start_time = form.start_time.data
        ev.end_time = form.end_time.data
        ev.description = form.description.data
        if ev.end_time <= ev.start_time:
            flash('End time must be after start time', 'danger')
            return render_template('event/edit.html', form=form, event=ev)
        conflicts = check_conflicts_for_event(ev)
        if conflicts:
            flash('Time change causes resource conflicts: ' + '; '.join(conflicts), 'danger')
            return render_template('event/edit.html', form=form, event=ev)
        db.session.commit()
        flash('Event updated', 'success')
        return redirect(url_for('event.list_events'))
    return render_template('event/edit.html', form=form, event=ev)

@bp.route('/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    ev = Event.query.get_or_404(event_id)
    db.session.delete(ev)
    db.session.commit()
    flash('Event deleted', 'info')
    return redirect(url_for('event.list_events'))

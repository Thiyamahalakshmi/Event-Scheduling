from flask import Blueprint, render_template, request
from ..models import Event, Resource, EventResourceAllocation
from datetime import datetime

bp = Blueprint('reports', __name__, template_folder='templates')

@bp.route('/resource-utilisation', methods=['GET','POST'])
def resource_utilisation():
    results = []
    start = None
    end = None
    if request.method == 'POST':
        start = datetime.fromisoformat(request.form['start'])
        end = datetime.fromisoformat(request.form['end'])
        resources = Resource.query.all()
        for r in resources:
            total_hours = 0.0
            upcoming = []
            allocs = EventResourceAllocation.query.filter_by(resource_id=r.resource_id).all()
            for a in allocs:
                ev = a.event
                overlap_start = max(ev.start_time, start)
                overlap_end = min(ev.end_time, end)
                if overlap_start < overlap_end:
                    hrs = (overlap_end - overlap_start).total_seconds() / 3600.0
                    total_hours += hrs * a.quantity
                if ev.start_time >= datetime.now():
                    upcoming.append(ev)
            results.append({'resource': r, 'total_hours': total_hours, 'upcoming': upcoming})
    return render_template('reports/resource_utilisation.html', results=results, start=start, end=end)

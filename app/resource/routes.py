from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models import Resource
from ..resource.forms import ResourceForm

bp = Blueprint('resource', __name__, template_folder='templates')

@bp.route('/')
def list_resources():
    resources = Resource.query.order_by(Resource.resource_name).all()
    return render_template('resource/list.html', resources=resources)

@bp.route('/create', methods=['GET','POST'])
def create_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        r = Resource(resource_name=form.resource_name.data, resource_type=form.resource_type.data, capacity=form.capacity.data)
        db.session.add(r)
        db.session.commit()
        flash('Resource created', 'success')
        return redirect(url_for('resource.list_resources'))
    return render_template('resource/create.html', form=form)

@bp.route('/<int:resource_id>/edit', methods=['GET','POST'])
def edit_resource(resource_id):
    r = Resource.query.get_or_404(resource_id)
    form = ResourceForm(obj=r)
    if form.validate_on_submit():
        r.resource_name = form.resource_name.data
        r.resource_type = form.resource_type.data
        r.capacity = form.capacity.data
        db.session.commit()
        flash('Resource updated', 'success')
        return redirect(url_for('resource.list_resources'))
    return render_template('resource/edit.html', form=form, resource=r)

@bp.route('/<int:resource_id>/delete', methods=['POST'])
def delete_resource(resource_id):
    r = Resource.query.get_or_404(resource_id)
    db.session.delete(r)
    db.session.commit()
    flash('Resource deleted', 'info')
    return redirect(url_for('resource.list_resources'))


from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import Event, Resource, EventResourceAllocation
from datetime import datetime, timedelta
import click

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("seed")
def seed():
    """Seed the database with sample data"""
    with app.app_context():
        if Resource.query.count() == 0:
            r1 = Resource(resource_name='Room A', resource_type='room', capacity=1)
            r2 = Resource(resource_name='Instructor Alice', resource_type='instructor', capacity=1)
            r3 = Resource(resource_name='Projector 1', resource_type='equipment', capacity=1)
            db.session.add_all([r1, r2, r3])
            db.session.commit()
        if Event.query.count() == 0:
            now = datetime.utcnow()
            ev1 = Event(title='Workshop 1', start_time=now, end_time=now.replace(hour=now.hour+2), description='Team workshop')
            ev2 = Event(title='Seminar 1', start_time=now+timedelta(days=1), end_time=now+timedelta(days=1, hours=2), description='Guest seminar')
            db.session.add_all([ev1, ev2])
            db.session.commit()
        ev1 = Event.query.first()
        r_room = Resource.query.filter_by(resource_name='Room A').first()
        if ev1 and r_room and EventResourceAllocation.query.count()==0:
            a1 = EventResourceAllocation(event_id=ev1.event_id, resource_id=r_room.resource_id, quantity=1)
            db.session.add(a1)
            db.session.commit()
        print('Seeding done.')

if __name__ == '__main__':
    print('Use flask CLI: flask run, flask db init/migrate/upgrade, flask seed')

from app import Task
from app import db, app

with app.app_context():
    db.create_all()

    if Task.query.count() == 0:
        tasks = [
            Task(name="Deploy App", description="Deploy the Flask app to the cloud.", is_done=False),
            Task(name="Optimize DB", description="Optimize the database access layer.", is_done=False),
            Task(name="Install AppSignal", description="Install AppSignal to track errors.", is_done=False),
        ]

        for task in tasks:
            db.session.add(task)

        db.session.commit()

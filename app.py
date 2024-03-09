from dotenv import load_dotenv
load_dotenv()

from __appsignal__ import appsignal  # noqa: E402
appsignal.start()

from flask import Flask, jsonify, request  # noqa: E402
from flask_sqlalchemy import SQLAlchemy  # noqa: E402

app = Flask(__name__)
app.secret_key = "9CB3Bphjkd99swIDHHfS1YMBHInkw1uC"
app.json.sort_keys = False

db = SQLAlchemy()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///default.db"
db.init_app(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(512), nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    is_done = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Task {self.id}>"


@app.route("/")
def list_view():
    tasks = Task.query.all()
    return jsonify([task.as_dict() for task in tasks])


@app.route("/<int:task_id>", methods=["GET"])
def detail_view(task_id):
    task = db.get_or_404(Task, task_id)
    return jsonify(task.as_dict())


@app.route("/create", methods=["POST"])
def create_view():
    name = request.form.get("name", type=str)
    description = request.form.get("description", type=str)

    task = Task(name=name, description=description)
    db.session.add(task)
    db.session.commit()

    return jsonify(task.as_dict()), 201


@app.route("/toggle-done/<int:task_id>", methods=["PATCH"])
def mark_done_view(task_id):
    task = db.get_or_404(Task, task_id)

    task.is_done = not task.is_done
    db.session.commit()

    return jsonify(task.as_dict())


@app.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_view(task_id):
    task = db.get_or_404(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({}), 204


@app.route("/statistics", methods=["GET"])
def statistics_view():
    done_tasks_count = Task.query.filter_by(is_done=True).count()
    undone_tasks_count = Task.query.filter_by(is_done=False).count()
    done_percentage = done_tasks_count / (done_tasks_count + undone_tasks_count) * 100

    return jsonify({
        "done_tasks_count": done_tasks_count,
        "undone_tasks_count": undone_tasks_count,
        "done_percentage": done_percentage,
    })


if __name__ == "__main__":
    app.run()

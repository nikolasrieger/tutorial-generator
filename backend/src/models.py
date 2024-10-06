from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    feedback_comments = db.relationship("Feedback", backref="prompt", lazy=True)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompt.id"), nullable=False)
    feedback_type = db.Column(db.String, nullable=False)
    comment = db.Column(db.Text, nullable=True)

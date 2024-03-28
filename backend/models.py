from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Submit {self.user} {self.score} {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'score': self.score,
            'date': self.date
        }
    
    def from_dict(self, data):
        for field in ['user', 'score', 'date']:
            if field in data:
                setattr(self, field, data[field])

    

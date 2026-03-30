"""Run db.create_all() — called by .ebextensions on deploy."""
from application import application
from app import db

with application.app_context():
    db.create_all()

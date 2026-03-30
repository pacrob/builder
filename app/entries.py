from collections import defaultdict
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash,
)

from app import db
from app.models import TimeEntry

entries_bp = Blueprint("entries", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@entries_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        task_name = request.form.get("task_name", "").strip()
        duration_raw = request.form.get("duration_minutes", "").strip()

        errors = []
        if not task_name:
            errors.append("Task name is required.")

        duration_minutes = None
        if not duration_raw:
            errors.append("Duration is required.")
        else:
            try:
                duration_minutes = int(duration_raw)
                if duration_minutes <= 0:
                    errors.append("Duration must be a positive integer.")
            except ValueError:
                errors.append("Duration must be a whole number.")

        if errors:
            for e in errors:
                flash(e)
        else:
            db.session.add(TimeEntry(task_name=task_name, duration_minutes=duration_minutes))
            db.session.commit()
            return redirect(url_for("entries.index"))

    all_entries = TimeEntry.query.order_by(TimeEntry.created_at.desc()).all()

    grouped = defaultdict(list)
    for entry in all_entries:
        grouped[entry.created_at.strftime("%Y-%m-%d")].append(entry)

    days = [
        {
            "date": date_str,
            "entries": grouped[date_str],
            "total_hours": round(sum(e.duration_minutes for e in grouped[date_str]) / 60, 2),
        }
        for date_str in sorted(grouped.keys(), reverse=True)
    ]

    return render_template("index.html", days=days)

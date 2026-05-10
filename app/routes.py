from flask import Blueprint, jsonify, request, current_app
from . import db
from .models import Trip, User
from flask_login import login_user, current_user, login_required

bp = Blueprint('routes', __name__)

@bp.route('/api/health')
def health():
    return jsonify({'status':'ok'})

@bp.route('/api/trips', methods=['GET','POST'])
def trips():
    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', 'Untitled')
        start = data.get('start')
        end = data.get('end')
        user = None
        if current_user and not current_user.is_anonymous:
            user = current_user
        trip = Trip(name=name, start=start or None, end=end or None, owner=user if user else None)
        db.session.add(trip)
        db.session.commit()
        return jsonify({'id': trip.id, 'name': trip.name, 'start': str(trip.start) if trip.start else None, 'end': str(trip.end) if trip.end else None}), 201
    else:
        trips = Trip.query.all()
        out = []
        for t in trips:
            out.append({'id':t.id,'name':t.name,'start':str(t.start) if t.start else None,'end':str(t.end) if t.end else None})
        return jsonify(out)


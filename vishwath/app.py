from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import requests

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:SGBR2024@localhost/schedule'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://flbkyrsudtcdkb:137b6a0124d64919d1a04144413773b6e3d123f34684a96d225f7be6bb29e83c@ec2-54-90-13-87.compute-1.amazonaws.com:5432/dfdvq49i0u2lnr?sslmode=require'



db=SQLAlchemy(app)
app.secret_key="hello"
app.permanent_session_lifetime= timedelta(minutes=5)


import csv

# A dictionary to quickly look up coordinates by location name
location_coords = {}

with open('static/BuildingInformation.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        location_coords[row['name']] = (row['latitude'], row['longitude'])

class Schedule(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    start =  db.Column(db.DateTime, nullable=False)
    loc = db.Column(db.String(120))



EVENTS = [
    {"name": "Workshop on AI", "start": "2025-04-01 10:00:00", "loc": "Room 101"},
    {"name": "Music Concert", "start": "2025-04-02 18:30:00", "loc": "Auditorium"}
]

@app.route('/event')
def event_page():
    return render_template('event.html', events=EVENTS)

@app.route('/add_to_schedule', methods=['POST'])
def add_to_schedule():
    event_name = request.form['name']
    event_datetime = request.form['start']
    event_location = request.form['loc']

    # Check if event is already scheduled
    existing_event = Schedule.query.filter_by(name=event_name, start=event_datetime).first()
    
    if not existing_event:
        new_event = Schedule(name=event_name, start=event_datetime, loc=event_location)
        db.session.add(new_event)
        db.session.commit()
        message = "Event added successfully!"
    else:
        message = "Event already added."

    return jsonify({"message": message})


@app.route("/")
def home():
    return render_template("ind.html")

@app.route("/route")
def route():
    return render_template('route.html')

@app.route("/event")
def event():
    return render_template('event.html')

@app.route("/google_map")
def google_map():
    route_start_points = [
        { "name": "Stoneridge Apartments", "lat": 29.620724476508645, "lng": -82.37546282465814 },
        { "name": "Greenwich Green Apartments", "lat": 29.616989987441865, "lng": -82.37431589666387 },
        { "name": "BLVD Apartments", "lat": 29.617468210928614, "lng": -82.37767025833176 },
    ]
    route_end_points = [
        { "name": "Reitz Uinon", "lat": 29.6467124109277, "lng": -82.34800087571728 },
        { "name": "CSE Building", "lat": 29.649290202565588, "lng": -82.3441214802752 },
        { "name": "MAE Building A", "lat": 29.643444744944144, "lng": -82.34822478920941 },
    ]
    return render_template('google_map.html', route_start_points=route_start_points, route_end_points=route_end_points)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        start = request.form['start']
        loc = request.form['loc']

        event_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M")
        schedule = Schedule(name=name, start=event_datetime, loc=loc)
        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for('schedule'))
    return render_template('add.html')

@app.route("/schedule", methods=['POST','GET'])
def schedule():
    schedule = Schedule.query.order_by(Schedule.start).all()
    return render_template('schedule.html', schedule=schedule)

@app.route("/generate",methods=['POST','GET'])
def generate():
    schedule = Schedule.query.order_by(Schedule.start).all()
    #put in api here
    API_KEY = 
    routes =[]
    for i in range(len(schedule)-1):
        start_loc = schedule[i].loc
        end_loc = schedule[i+1].loc

        start_coords = location_coords.get(start_loc)
        end_coords = location_coords.get(end_loc)
        if start_coords and end_coords:
            origin = f"{start_coords[0]},{start_coords[1]}"
            destination = f"{end_coords[0]},{end_coords[1]}"

            url = (
                f"https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={origin}&destination={destination}&mode=transit&transit_mode=bus&key={API_KEY}"
            )

            response = requests.get(url)
            data = response.json()

            if data['status'] == 'OK':
                steps = data['routes'][0]['legs'][0]['steps']
                bus_steps = []
                for step in steps:
                    if step['travel_mode'] == 'TRANSIT':
                        bus_info = {
                            "line_name": step['transit_details']['line']['short_name'],
                            "departure_stop": step['transit_details']['departure_stop']['name'],
                            "arrival_stop": step['transit_details']['arrival_stop']['name']
                        }
                        bus_steps.append(bus_info)
                routes.append({
                "start_location": start_loc,
                "bus_steps": bus_steps
                })
            else:
                routes.append({
                "start_location": start_loc,
                "bus_steps": []
                })  # No route found
        else:
            routes.append({
                "start_location": start_loc,
                "bus_steps": []
            })  # Missing coordinates
    routes.append({
        "start_location": schedule[len(schedule)-1].loc,
        "bus_steps": []
    })
    return render_template('generate.html', schedule=schedule,routes=routes)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    schedule = Schedule.query.get_or_404(id)
    if request.method == 'POST':
        schedule.name = request.form['name']
        start = request.form['start']
        event_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M")
        schedule.start = event_datetime
        schedule.loc = request.form['loc']
        db.session.commit()
        return redirect(url_for('schedule'))
    return render_template('edit.html', schedule=schedule)

@app.route('/delete/<int:id>')
def delete(id):
    schedule = Schedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    return redirect(url_for('schedule'))




if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.debug=True
    app.run()
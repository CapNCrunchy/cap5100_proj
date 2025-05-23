from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import requests
import pandas as pd

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:nasatlx@localhost/schedule'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://flbkyrsudtcdkb:137b6a0124d64919d1a04144413773b6e3d123f34684a96d225f7be6bb29e83c@ec2-54-90-13-87.compute-1.amazonaws.com:5432/dfdvq49i0u2lnr?sslmode=require'



db=SQLAlchemy(app)
app.secret_key="hello"
app.permanent_session_lifetime= timedelta(minutes=5)


import csv

# A dictionary to quickly look up coordinates by location name
location_coords = {}
route_start_points = []

with open("C:/Users/kshar/Desktop/uf/2025_spring/hci/cap5100_proj/vishwath/static/BuildingInformation.csv", newline='') as csvfile:

    reader = csv.DictReader(csvfile)
    for row in reader:
        location_coords[row['name']] = (row['latitude'], row['longitude'])
        if row['name'] and row['latitude'] and row['longitude']:
            route_start_points.append({'name': row['name'], 'lat': float(row['latitude']), 'lng': float(row['longitude'])})

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
    return render_template('google_map.html', route_start_points=route_start_points)

@app.route('/add', methods=['GET', 'POST'])
def add():
    locations_df = pd.read_csv('C:/Users/kshar/Desktop/uf/2025_spring/hci/cap5100_proj/vishwath/static/BuildingInformation.csv')  # Update with your path
    locations_list = locations_df['name'].tolist()  # Update with your column name
    if request.method == 'POST':
        name = request.form['name']
        start = request.form['start']
        loc = request.form['loc']

        event_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M")
        schedule = Schedule(name=name, start=event_datetime, loc=loc)
        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for('schedule'))
    return render_template('add.html',locations=locations_list)

@app.route("/schedule", methods=['POST','GET'])
def schedule():
    schedule = Schedule.query.order_by(Schedule.start).all()
    return render_template('schedule.html', schedule=schedule)

@app.route("/generate",methods=['POST','GET'])
def generate():
    schedule = Schedule.query.order_by(Schedule.start).all()
    #put in api here
    API_KEY = ""
    routes =[]
    start_coords = []
    end_coords = []

    event_times = []
    bus_route_all_legs = []

    for i in range(len(schedule)-1):
        start_loc = schedule[i].loc
        end_loc = schedule[i+1].loc
        start_coords = location_coords.get(start_loc)
        end_coords = location_coords.get(end_loc)
        if schedule[i].start:
            event_times.append(schedule[i].start.strftime('%Y-%m-%dT%H:%M:%S'))
        else:
            event_times.append(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        print(event_times)


        if start_coords and end_coords:
            origin = f"{start_coords[0]},{start_coords[1]}"
            destination = f"{end_coords[0]},{end_coords[1]}"

            bus_route_all_legs.append((i,
                                    {'lat': float(start_coords[0]) , 'lng': float(start_coords[1])},
                                    {'lat': float(end_coords[0]) , 'lng': float(end_coords[1])}))

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
                "bus_steps": bus_steps,
                "route_id": i,
                })
            else:
                routes.append({
                "start_location": start_loc,
                "bus_steps": [],
                    "route_id": i,
                })  # No route found
        else:
            routes.append({
                "start_location": start_loc,
                "bus_steps": [],
                    "route_id": i,
            })  # Missing coordinates

            # If location is not provided, just use the location of UF.
            bus_route_all_legs.append((i, { "lat": 29.6467, "lng": -82.3532 }, { "lat": 29.6467, "lng": -82.3532 }))


    routes.append({
        "start_location": schedule[len(schedule)-1].loc,
        "bus_steps": [],
        "route_id": len(schedule)-1,
    })
    return render_template('generate.html', schedule=schedule,routes=routes,
                            route_legs=bus_route_all_legs, event_times=event_times)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    locations_df = pd.read_csv('C:/Users/kshar/Desktop/uf/2025_spring/hci/cap5100_proj/vishwath/static/BuildingInformation.csv')  # Update with your path
    locations_list = locations_df['name'].tolist()  # Update with your column name
    schedule = Schedule.query.get_or_404(id)
    if request.method == 'POST':
        schedule.name = request.form['name']
        start = request.form['start']
        event_datetime = datetime.strptime(start, "%Y-%m-%dT%H:%M")
        schedule.start = event_datetime
        schedule.loc = request.form['loc']
        db.session.commit()
        return redirect(url_for('schedule'))
    return render_template('edit.html', schedule=schedule, locations=locations_list)

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
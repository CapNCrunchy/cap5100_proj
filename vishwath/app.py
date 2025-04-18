from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:SGBR2024@localhost/schedule'
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://flbkyrsudtcdkb:137b6a0124d64919d1a04144413773b6e3d123f34684a96d225f7be6bb29e83c@ec2-54-90-13-87.compute-1.amazonaws.com:5432/dfdvq49i0u2lnr?sslmode=require'



db=SQLAlchemy(app)
app.secret_key="hello"
app.permanent_session_lifetime= timedelta(minutes=5)




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
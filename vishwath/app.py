from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/schedule'
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


event = [[1, "A", "Math", "11 Feb 1980", "123 candy street", "123","vishwath.ram@gmail.com"],
         [2, "B", "Physics", "17 Nov 1985", "234 apple street", "123","vishwath.ram@gmail.com"],
         [3, "C", "Chemistry", "26 Mar 1976", "345 star apartments", "123","vishwath.ram@gmail.com"],
         [4, "D", "Computer Science", "05 May 1984", "567 new street", "123","vishwath.ram@gmail.com"],
         [5, "E", "English", "21 Oct 1982", "798 old apartments", "123","vishwath.ram@gmail.com"]]

comment_no=0

@app.route("/")
def home():
    return render_template("schedule.html")



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
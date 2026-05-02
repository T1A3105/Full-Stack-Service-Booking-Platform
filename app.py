from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    service = db.Column(db.String(100))
    date = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    service = request.form['service']
    date = request.form['date']

    new_booking = Booking(name=name, service=service, date=date)
    db.session.add(new_booking)
    db.session.commit()

    return redirect('/bookings')

@app.route('/bookings')
def bookings():
    all_bookings = Booking.query.all()
    return render_template("bookings.html", bookings=all_bookings)

# ✅ DELETE
@app.route('/delete/<int:id>')
def delete(id):
    booking = Booking.query.get(id)
    db.session.delete(booking)
    db.session.commit()
    return redirect('/bookings')

# ✅ EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    booking = Booking.query.get(id)

    if request.method == 'POST':
        booking.name = request.form['name']
        booking.service = request.form['service']
        booking.date = request.form['date']

        db.session.commit()
        return redirect('/bookings')

    return render_template("edit.html", booking=booking)

if __name__ == "__main__":
    app.run()
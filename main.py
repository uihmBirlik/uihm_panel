from flask import Flask, request, render_template, jsonify
import csv

app = Flask(__name__)


def csv_to_dict(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        return {rows[0]: int(rows[1]) for rows in reader if len(rows) >= 2}


attendance = csv_to_dict("names.csv")


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/get_attendees")
def get_attendees():
    with open("attendees.txt", "r") as names:
        attendees = names.readlines()
        return jsonify(attendees)


@app.route('/mark', methods=['POST'])
def mark():
    ad = request.form.get('attendee')
    if ad in attendance:
        attendance[ad] += 1
    else:
        attendance[ad] = 1
    with open("names.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Attendances"])
        for name, value in attendance.items():
            writer.writerow(([name, value]))
    return render_template('marked.html', name=ad)


@app.route('/attendance')
def show_attendance():
    return render_template('attendance.html', attendance=attendance)


if __name__ == '__main__':
    app.run(debug=True)

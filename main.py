from flask import Flask, request, render_template, jsonify, session
import csv
import time

app = Flask(__name__)
app.secret_key = "idrissaRusongeka"


def csv_to_dict(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        return {rows[0]: int(rows[1]) for rows in reader if len(rows) >= 2}


attendance = csv_to_dict("names.csv")


@app.route('/')
def index():
    print(session.get("last_vist"))
    last_visit = session.get("last_vist", 0)
    current_time = int(time.time())
    if current_time - last_visit < 300:
        return jsonify(error="access denied"), 404
    else:
        session["last_vist"] = current_time
        return render_template('index.html'), 200


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

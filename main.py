from datetime import datetime

from flask import Flask, request, render_template, jsonify, json
import csv

app = Flask(__name__)
attendance_data = {}


def csv_to_dict(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        return {rows[0]: int(rows[1]) for rows in reader if len(rows) >= 2}


attendance = csv_to_dict("names.csv")


@app.route('/', methods=["GET"])
def index():
    # Get the client's IP address
    client_ip = request.remote_addr
    print(client_ip)

    # Check if the IP address is in the attendance data
    if client_ip in attendance_data:
        # Get the last access time for this IP address
        last_access = attendance_data[client_ip]

        # Calculate the time difference in minutes
        time_diff = (datetime.now() - last_access).total_seconds() / 60

        # If the time difference is less than 5 minutes, return an error message
        if time_diff < 5:
            return json.dumps({"error": "Please wait before accessing the system again"}), 429

        # If the time difference is 5 minutes or more, update the access time
        attendance_data[client_ip] = datetime.now()
    else:
        # If the IP address is not in the attendance data, add it
        attendance_data[client_ip] = datetime.now()

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

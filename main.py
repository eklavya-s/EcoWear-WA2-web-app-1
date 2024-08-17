from flask import Flask, render_template, redirect, url_for, session, request
import csv

app = Flask(__name__)
app.secret_key = "EcoWear"

def read_user_data():
    user_data = {}
    with open("user_data.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            username = row[0]
            password = row[1]
            total_points = int(row[2])
            completed_quizzes = row[3].split(",") if row[3] else []
            user_data[username] = {
                "password": password,
                "total_points": total_points,
                "completed_quizzes": completed_quizzes
            }
    return user_data

def write_user_data(user_data):
    with open("user_data.csv", "w", newline="") as file:
        file.write("username,password,total_points,completed_quizzes\n")  # Adding header
        for username, data in user_data.items():
            completed_quizzes_str = ",".join(data["completed_quizzes"])
            file.write(f"{username},{data['password']},{data['total_points']},{completed_quizzes_str}\n")

@app.route("/")
def homepage():
    if "username" not in session:
        return redirect("/login")
    username = session.get("username")
    user_data = read_user_data()
    total_points = user_data.get(username, {}).get("total_points", 0)
    return render_template("homepage.html", total_points=total_points)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = read_user_data()
        if username in user_data:
            return "Username already exists"
        user_data[username] = {"password": password, "total_points": 0, "completed_quizzes": []}
        write_user_data(user_data)
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = read_user_data()
        if username not in user_data:
            return redirect("/register")
        elif user_data[username]["password"] != password:
            return "Invalid credentials"
        session["username"] = username
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/quiz1", methods=["POST"])
def quiz1():
    username = session.get("username")
    user_data = read_user_data()
    if "quiz1" in user_data.get(username, {}).get("completed_quizzes", []):
        return "You have already completed Quiz 1.", 403
    return render_template("quiz1.html")

@app.route("/quiz2", methods=["POST"])
def quiz2():
    username = session.get("username")
    user_data = read_user_data()
    if "quiz2" in user_data.get(username, {}).get("completed_quizzes", []):
        return "You have already completed Quiz 2.", 403
    return render_template("quiz2.html")

@app.route("/quiz3", methods=["POST"])
def quiz3():
    username = session.get("username")
    user_data = read_user_data()
    if "quiz3" in user_data.get(username, {}).get("completed_quizzes", []):
        return "You have already completed Quiz 3.", 403
    return render_template("quiz3.html")

def update_user_points(username, additional_points, quiz_name):
    user_data = read_user_data()
    if username in user_data:
        user_data[username]["total_points"] += additional_points
        user_data[username]["completed_quizzes"].append(quiz_name)
    write_user_data(user_data)

@app.route("/quiz1_submit", methods=["POST"])
def quiz1_submit():
    answers = {
        "q1": "B",
        "q2": "C",
        "q3": "C",
        "q4": "C",
        "q5": "C",
        "q6": "A",
        "q7": "C",
        "q8": "C",
        "q9": "C",
        "q10": "D"
    }
    username = session.get("username")
    total_points = 0
    for question, correct_answer in answers.items():
        if request.form.get(question) == correct_answer:
            total_points += 5
    update_user_points(username, total_points, "quiz1")
    return redirect("/")

@app.route("/quiz2_submit", methods=["POST"])
def quiz2_submit():
    answers = {
        "q1": "B",
        "q2": "B",
        "q3": "C",
        "q4": "C",
        "q5": "C",
        "q6": "A",
        "q7": "C",
        "q8": "C",
        "q9": "C",
        "q10": "D"
    }
    username = session.get("username")
    total_points = 0
    for question, correct_answer in answers.items():
        if request.form.get(question) == correct_answer:
            total_points += 5
    update_user_points(username, total_points, "quiz2")
    return redirect("/")

@app.route("/quiz3_submit", methods=["POST"])
def quiz3_submit():
    answers = {
        "q1": "B",
        "q2": "C",
        "q3": "C",
        "q4": "C",
        "q5": "C",
        "q6": "A",
        "q7": "C",
        "q8": "C",
        "q9": "C",
        "q10": "D"
    }
    username = session.get("username")
    total_points = 0
    for question, correct_answer in answers.items():
        if request.form.get(question) == correct_answer:
            total_points += 5
    update_user_points(username, total_points, "quiz3")
    return redirect("/")

@app.route("/leaderboard")
def leaderboard():
    user_data = read_user_data()
    unsorted_leaderboard = [(username, user_data[username]["total_points"]) for username in user_data]
    sorted_leaderboard = sorted(unsorted_leaderboard, key=lambda x: x[1], reverse=True)
    return render_template("leaderboard.html", sorted_leaderboard=sorted_leaderboard)

def voucher_csv():
    brands = []
    with open("voucher.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            brands.append({"brand": row[0], "voucher": row[1]})
    return brands

@app.route('/redeem', methods=['GET', 'POST'])
def redeem():
    user_data = read_user_data()
    username = session.get('username')
    total_points = user_data.get(username, {}).get('total_points', 0)
    brands = voucher_csv()

    if request.method == 'POST':
        brand = request.form['brand']
        if total_points >= 500:
            voucher_code = None # inititalise
            for store in brands:
                if store['brand'] == brand:
                    voucher_code = store['voucher']
                    break

            # deduct points 
            if voucher_code:
                user_data[username]['total_points'] -= 500
                write_user_data(user_data)
                session['voucher_code'] = voucher_code
                return redirect('/voucher_show')
        else:
            return redirect("/redeem")
    return render_template('redeem.html', total_points=total_points, brands=brands)

@app.route('/voucher_show')
def voucher_show():
    voucher_code = session.get('voucher_code')
    return render_template('voucher_show.html', voucher_code=voucher_code)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
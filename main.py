from flask import Flask, render_template, redirect, url_for, session, request
import csv

app = Flask(__name__)
app.secret_key = 'EcoWear'

# Global dictionary to store user data
user_data = {
    'eklavya': {
        "total_points": 1000,  # example points
        "completed_quizzes": ['Quiz1', 'Quiz2']  # example completed quizzes
    }
}

@app.route('/')
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session.get('username')
    total_points = user_data.get(username, {}).get('total_points', 0)
    total_quizes_done = len(user_data.get(username, {}).get('completed_quizzes', []))
    return render_template("homepage.html", total_points=total_points, total_quizes_done=total_quizes_done)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        if username not in user_data:
            user_data[username] = {"total_points": 0, "completed_quizzes": []}
        return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
    

@app.route('/quiz1', methods=['POST'])
def quiz1():
    username = session.get('username')
    if 'quiz1' in user_data.get(username, {}).get('completed_quizzes', []):
        return "You have already completed Quiz 1.", 403
    return render_template('quiz1.html')

@app.route('/quiz2', methods=['POST'])
def quiz2():
    username = session.get('username')
    if 'quiz2' in user_data.get(username, {}).get('completed_quizzes', []):
        return "You have already completed Quiz 2.", 403
    return render_template('quiz2.html')

@app.route('/quiz3', methods=['POST'])
def quiz3():
    username = session.get('username')
    if 'quiz3' in user_data.get(username, {}).get('completed_quizzes', []):
        return "You have already completed Quiz 3.", 403
    return render_template('quiz3.html')

def update_user_points(username, additional_points, quiz_name):
    if username in user_data:
        user_data[username]['total_points'] += additional_points
        user_data[username]['completed_quizzes'].append(quiz_name)
    else:
        user_data[username] = {
            "total_points": additional_points,
            "completed_quizzes": [quiz_name]
        }

@app.route('/quiz1_submit', methods=['POST'])
def quiz1_submit():
    answers = {
        'q1': 'B',
        'q2': 'C',
        'q3': 'C',
        'q4': 'C',
        'q5': 'C',
        'q6': 'A',
        'q7': 'C',
        'q8': 'C',
        'q9': 'C',
        'q10': 'D'
    }

    username = session.get('username')
    total_points = 0

    for question, correct_answer in answers.items():
        if request.form.get(question) == correct_answer:
            total_points += 5

    update_user_points(username, total_points, 'quiz1')
    return redirect('/')

@app.route('/quiz2_submit', methods=['POST'])
def quiz2_submit():
    answers = {
        'q1': 'B',
        'q2': 'B',
        'q3': 'C',
        'q4': 'C',
        'q5': 'C',
        'q6': 'A',
        'q7': 'C',
        'q8': 'C',
        'q9': 'C',
        'q10': 'D'
    }

    username = session.get('username')
    total_points = 0

    for question, correct_answer in answers.items():
        if request.form.get(question) == correct_answer:
            total_points += 5

    update_user_points(username, total_points, 'quiz2')
    return redirect('/')

@app.route('/quiz3_submit', methods=['POST'])
def quiz3_submit():
    answers = {
        'q1': 'B',
        'q2': 'C',
        'q3': 'C',
        'q4': 'C',
        'q5': 'C',
        'q6': 'A',
        'q7': 'C',
        'q8': 'C',
        'q9': 'C',
        'q10': 'D'
    }

    username = session.get('username')
    total_points = 0

    for question, correct_answer in answers.items():
        if request.form.get(question) == correct_answer:
            total_points += 5

    update_user_points(username, total_points, 'quiz3')
    return redirect('/')

@app.route('/leaderboard')
def leaderboard():
    unsorted_leaderboard = [(username, user_data[username]['total_points']) for username in user_data]
    sorted_leaderboard = sorted(unsorted_leaderboard, key=lambda x:x[1], reverse=True)
    return render_template("leaderboard.html", sorted_leaderboard=sorted_leaderboard)

def voucher_csv():
    brands = []
    with open('voucher.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header
        for row in reader:
            brands.append({"brand": row[0], "voucher": row[1]})
    return brands
        
@app.route('/redeem', methods=['GET', 'POST'])
def redeem():
    username = session.get('username')
    total_points = user_data.get(username, {}).get('total_points', 0)
    brands = voucher_csv()

    if request.method == 'POST':
        brand = request.form['brand']
        if total_points >= 500:
            voucher_code = None # inititalise
            for item in brands:
                if item['brand'] == brand:
                    voucher_code = item['voucher']
                    break

            # deduct points 
            if voucher_code:
                user_data[username]['total_points'] -= 500
                session['voucher_code'] = voucher_code
                return redirect('/voucher_show')
        else:
            return redirect("/redeem")

    return render_template('redeem.html', total_points=total_points, brands=brands)

@app.route('/voucher_show')
def voucher_show():
    voucher_code = session.get('voucher_code')
    return render_template('voucher_show.html', voucher_code=voucher_code)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
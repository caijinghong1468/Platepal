from flask import Blueprint, render_template, request, redirect, flash, url_for, abort # type: ignore
from database import db

user = Blueprint("user", __name__)

@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_acc = request.form['user_acc']
        user_password = request.form['user_password']

        cursor = db.connection.cursor()
        try:
            # Check if the account already exists
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM USERS
                WHERE Account = '{user_acc}';
            """)
            result = cursor.fetchone()
            if result[0] > 0:  # If the account already exists
                flash("Account already exists. Please choose a different account.")
                return redirect(url_for('user.register'))

            # Insert the new user into the database
            cursor.execute(f"""
                INSERT INTO USERS (UName, Account, Password)
                VALUES ('{user_name}', '{user_acc}', '{user_password}');
            """)
            db.connection.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for('user.login'))  # Redirect to login after registration
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK")
            cursor.close()
            abort(500, "An error occurred during registration.")
    return render_template('register.html')

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_acc = request.form['user_acc']
        user_password = request.form['user_password']

        cursor = db.connection.cursor()
        try:
            # Query to check if the account and password match
            cursor.execute(f"""
                SELECT ID
                FROM USERS
                WHERE Account = '{user_acc}' AND Password = '{user_password}';
            """)
            result = cursor.fetchone()  # Fetch one result
            cursor.close()

            if result:  # If a matching user is found
                user_id = result[0]
                return redirect(url_for('user.profile', user_id=user_id))
            else:  # If no matching user is found
                flash("Invalid account or password. Please try again.")
                return redirect(url_for('user.login'))
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK")
            cursor.close()
            abort(500, "An error occurred during login.")
    return render_template('login.html')

@user.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    cursor = db.connection.cursor()
    try:
        # Fetch user data from the database
        cursor.execute(f"""
            SELECT UName, Gender, Age, Height, Weight
            FROM USERS
            WHERE ID = '{user_id}';
        """)
        user_data = cursor.fetchone()  # Fetch one result
        cursor.close()
        if not user_data:
            abort(404, "User not found.")
        return render_template('user_home.html', user_data=user_data, user_id=user_id)
    except Exception as e:
        print(e)
        abort(500, "An error occurred while fetching user data.")


@user.route('/user_info/<int:user_id>', methods=['GET', 'POST'])
def user_info(user_id):
    cursor = db.connection.cursor()
    if request.method == 'POST':
        try:
            # Collect and process form data
            user_name = request.form['user_name']
            user_gender = request.form['user_gender']
            user_age = int(request.form['user_age'])  # Convert to integer
            user_height = float(request.form['user_height'])  # Convert to float
            user_weight = float(request.form['user_weight'])  # Convert to float

            # Map gender values for the database
            gender_map = {
                "Male": "M",
                "Female": "F",
                "Other": None  # None will be converted to NULL in the database
            }
            user_gender_db = gender_map.get(user_gender)

            # Update user information in the database
            cursor.execute("""
                UPDATE USERS
                SET UName = %s, Gender = %s, Age = %s, Height = %s, Weight = %s
                WHERE ID = %s;
            """, (user_name, user_gender_db, user_age, user_height, user_weight, user_id))
            db.connection.commit()

            flash("User information updated successfully!")
        except Exception as e:
            print(f"Error updating user: {e}")
            db.connection.rollback()
            abort(500, "An error occurred while updating user data.")
        finally:
            cursor.close()
        return redirect(url_for('user.user_info', user_id=user_id))

    try:
        # Fetch user data from the database
        cursor.execute("""
            SELECT UName, Gender, Age, Height, Weight
            FROM USERS
            WHERE ID = %s;
        """, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()

        if not user_data:
            abort(404, "User not found.")
        
        return render_template('user_info.html', user_data=user_data, user_id=user_id)
    except Exception as e:
        print(f"Error fetching user data: {e}")
        abort(500, "An error occurred while fetching user data.")

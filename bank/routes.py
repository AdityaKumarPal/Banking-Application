from bank import app
from flask import render_template, redirect, url_for, flash, session
from bank.forms import RegisterForm, LoginForm, DepositForm, WithdrawalForm, TransferForm, ChangePasswordForm
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="your_mysql_password", database="database_name")


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route('/register', methods=["GET", "POST"])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        gender = form.gender.data
        dob = form.dob.data
        email = form.email_address.data
        mobile = form.mobile.data
        password = form.password1.data
        confirm_password = form.password2.data
        query = ("insert into users(name, gender, dob, email, mobile, password, confirm_password) values(%s, %s, "
                 "%s, %s, %s, %s, %s)")
        data_query = (name, gender, dob, email, mobile, password, confirm_password)
        cursor = mydb.cursor()
        cursor.execute(query, data_query)
        mydb.commit()
        flash("Your account is created successfully.", category="success")
        return redirect(url_for('login_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category="danger")

    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            cursor = mydb.cursor()
            cursor.execute("select Password from users where Mobile = '{}';".format(form.mobile.data))
            passwrd = cursor.fetchone()[0]

            my_cursor = mydb.cursor()
            my_cursor.execute("select Name from users where Mobile = '{}';".format(form.mobile.data))
            my_name = my_cursor.fetchone()[0]

            if passwrd == form.password.data:
                flash(f"You are logged in successfully as: {my_name}", category="success")
                session['loggedin'] = True
                session['username'] = my_name
                return redirect(url_for('info_page'))
            else:
                flash("Incorrect Username or Password! Please try again.", category="danger")

        except:
            flash("Your account does not exist!", category="danger")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        gender = form.gender.data
        dob = form.dob.data
        email = form.email_address.data
        mobile = form.mobile.data
        password = form.password1.data
        confirm_password = form.password2.data
        query = (
            "insert into users(Name, Gender, DOB, Email, Mobile, Password, Confirm_Password) values(%s, %s, %s, %s, %s, %s, %s)")
        data_query = (name, gender, dob, email, mobile, password, confirm_password)
        cursor = mydb.cursor()
        cursor.execute(query, data_query)
        mydb.commit()
        flash("Your account is created successfully.", category="success")
        return redirect(url_for('login_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category="danger")

    return render_template("register.html", form=form)


@app.route('/info')
def info_page():
    my_cursor = mydb.cursor()
    my_cursor.execute(f"select Mobile from users where Name = '{session['username']}'")
    Mob = my_cursor.fetchone()[0]

    global Total_Cash
    cursor = mydb.cursor()
    cursor.execute(f"select SUM(Cash) from transactions where mobile = '{Mob}'")
    Total_Cash = cursor.fetchone()[0]

    return render_template("loggedin/info.html", username=session['username'], Total_Cash=Total_Cash)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash("You have successfully logged out! Thank you for using ABI bank.", category="info")
    return redirect(url_for('login_page'))

@app.route('/deposit', methods=['GET', 'POST'])
def deposit_page():
    form = DepositForm()

    if form.validate_on_submit():
        if session['loggedin']:
            my_cursor = mydb.cursor()
            my_cursor.execute("select Mobile from users where Name = '{}'".format(session['username']))
            my_num = my_cursor.fetchone()[0]

            if form.cash.data > 0:
                cursor = mydb.cursor()
                cursor.execute(
                    "insert into transactions(Transaction, Transferred, Cash, mobile) values('Deposit', '-', {}, '{}')".format(
                        form.cash.data, my_num))
                mydb.commit()
                flash("Your cash is deposit successfully.", category="success")
                return redirect(url_for('info_page'))
            else:
                flash("Enter a valid amount.", category="danger")

    return render_template("loggedin/deposit.html", form=form, username=session['username'], Total_Cash=Total_Cash)


@app.route('/statement')
def statement_page():
    if session['loggedin']:
        cursor = mydb.cursor()
        cursor.execute(
            f"select users.Name, transactions.Transaction, transactions.Transferred, transactions.Cash, transactions.Date_Time from users, transactions where (users.Mobile = transactions.mobile and users.Name = '{session['username']}')")
        user = cursor.fetchall()
        return render_template("loggedin/mini_statement.html", userDetails=user, username=session['username'],
                               Total_Cash=Total_Cash)
    else:
        return redirect(url_for('info_page'))


@app.route('/transfer', methods=['GET', 'POST'])
def transfer_page():
    form = TransferForm()
    if form.validate_on_submit():
        try:
            if session['loggedin']:
                my_cursor = mydb.cursor()
                my_cursor.execute("select Mobile from users where Name = '{}'".format(session['username']))
                my_num = my_cursor.fetchone()[0]

                new_cursor = mydb.cursor()
                new_cursor.execute(f"select Name from users where Mobile = '{form.recipient.data}'")
                recipient_name = new_cursor.fetchone()[0]

                if Total_Cash >= form.cash.data:

                    M_cursor = mydb.cursor()
                    M_cursor.execute(
                        "insert into transactions(Transaction, Transferred, Cash, mobile) values('Transfer to', '{}', -{}, '{}')".format(
                            recipient_name, form.cash.data, my_num))
                    mydb.commit()

                    mera_cursor = mydb.cursor()
                    mera_cursor.execute(
                        "insert into transactions(Transaction, Transferred, Cash, mobile) values('Transferred by', '{}', {}, '{}')".format(
                            session['username'], form.cash.data, form.recipient.data))
                    mydb.commit()

                    flash("Your cash transferred successfully.", category="success")
                    return redirect(url_for('info_page'))

                else:
                    flash("You have insufficient balance to make transaction.", category="danger")
                    return redirect(url_for('info_page'))

        except:
            flash(f"The recipient's account does not exist.", category="danger")

    return render_template("loggedin/transfer.html", form=form, username=session['username'], Total_Cash=Total_Cash)


@app.route('/withdrawal', methods=['GET', 'POST'])
def withdrawal_page():
    form = WithdrawalForm()
    if form.validate_on_submit():
        if session['loggedin']:
            my_cursor = mydb.cursor()
            my_cursor.execute("select Mobile from users where Name = '{}'".format(session['username']))
            my_num = my_cursor.fetchone()[0]

            if Total_Cash >= form.cash.data:
                if form.cash.data > 0:
                    cursor = mydb.cursor()
                    cursor.execute("insert into transaction(Transaction, Transferred, Cash, mobile)"
                                " values('Withdrawal', '-', -{}, '{}')".format(form.cash.data, my_num))
                    mydb.commit()

                    flash("Your cash is Withdrawal successfully.", category="success")
                    return redirect(url_for('info_page'))
                else:
                    flash("Enter a valid amount.", category="danger")
            else:
                flash("You have insufficient balance to make transaction.", category="danger")
                return redirect(url_for('info_page'))

    return render_template("loggedin/withdrawal.html", form=form, username=session['username'], Total_Cash=Total_Cash)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if session['loggedin']:
            cursor = mydb.cursor()
            cursor.execute("select Password from users where Name = '{}'".format(session['username']))
            my_pass = cursor.fetchone()[0]


            if form.oldPassword.data == my_pass:
                if form.newPassword.data == form.reEnterPassword.data:
                    cursor = mydb.cursor()
                    cursor.execute(
                        "update users set Password='{}', Confirm_Password='{}' where Name = '{}'".format(form.newPassword.data, form.reEnterPassword.data, session['username']))
                    mydb.commit()
                    flash("Your Password changed successfully.", category="success")
                    return redirect(url_for('info_page'))
                else:
                    flash("Password doesnot matches.", category="danger")
            else:
                flash("Please enter correct password.", category="danger")

    return render_template("loggedin/change_password.html", form=form, username=session['username'])


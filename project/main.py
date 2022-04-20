import numpy as np
import pandas as pd, sqlite3,csv
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from sqlalchemy import func, create_engine
from .models import Users, Deposits
from . import db
from datetime import datetime as dt

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')



@main.route("/redirect")
def redirecting():
    return render_template("admin.html")



@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.Name)


@main.route('/deposits')
@login_required
def deposits():
    return render_template('deposits.html')


@main.route("/deposits", methods=["POST"])
@login_required
def add_deposits():
    name=request.form.get("name")
    email = request.form.get("email")
    age = request.form.get("age")
    dob = request.form.get("DOB")
    # fdno = request.form.get("fdnumber")
    bank = request.form.get("bank")
    amount= request.form.get("amount")
    interest= request.form.get("interest")
    maturity= request.form.get("maturity")

    User= Users.query.filter_by(Email=email).first()

    new_fd = Deposits( Name=name, Email=email, Age=age,DOB=dt.strptime(dob,"%Y-%m-%d"),
                      BankName=bank, Amount=amount, Interest=interest, Maturity=maturity)

    if User:
        flash("FD Created")
        db.session.add(new_fd)
        db.session.commit()
        return render_template("admin.html")
    elif User is None:
        flash("Not an User!")
        return render_template("admin.html")

    return render_template("admin.html")


@main.route("/get_deposits" , methods=["GET"])
@login_required
def reports():
    deposits=Deposits.query.all()
    output = []
    for deposit in deposits:
        deposit_data = {}
        deposit_data["FD_Number"] = deposit.id
        deposit_data["Name"] = deposit.Name
        deposit_data["Email"] = deposit.Email
        deposit_data["Age"] = deposit.Age
        deposit_data["DOB"] = deposit.DOB
        deposit_data["BankName"] = deposit.BankName
        deposit_data["Amount_Rupees"] = deposit.Amount
        deposit_data["Interest_Rupees"] = deposit.Interest
        deposit_data["Maturity_Rupees"] = deposit.Maturity
        output.append(deposit_data)


    return render_template("reports.html",outputs=output)

@main.route("/exports")
@login_required
def exports():
    deposits = Deposits.query.all()
    output = []
    count = 0
    for deposit in deposits:
        deposit_data = {}
        deposit_data["FD_Number"] = deposit.id
        deposit_data["Name"] = deposit.Name
        deposit_data["Email"] = deposit.Email
        deposit_data["Age"] = deposit.Age
        deposit_data["DOB"] = deposit.DOB
        deposit_data["BankName"] = deposit.BankName
        deposit_data["Amount_Rupees"] = deposit.Amount
        deposit_data["Interest_Rupees"] = deposit.Interest
        deposit_data["Maturity_Rupees"] = deposit.Maturity
        output.append(deposit_data)
        count += 1

    df1 = pd.DataFrame(output)
    df1.to_csv("csvreports/adminreports.csv", index=False)

    plt.style.use('bmh')
    my_conn = create_engine("sqlite:///project\\bankly.sqlite")
    query = "SELECT  COUNT(id) as id , Email, Name FROM Deposits GROUP BY Email;"
    df = pd.read_sql(query, my_conn)
    x = df['Name']
    y = df["id"]
    plt.ylim(0, count)
    plt.yticks(np.arange(0, count + 4, 1.0))
    plt.xlabel('Name', fontsize=18)
    plt.title("Fixed Deposits of Users")
    plt.ylabel('Number of Fixed Deposits', fontsize=18)
    plt.bar(x, y)
    plt.show()
    return render_template("reports.html", outputs=output)



@main.route("/update/<int:FD_Number>" , methods=["GET", "POST"])
@login_required
def update(FD_Number):
    if request.method=="GET":
        deposit = Deposits.query.filter_by(id=FD_Number).first()
        output=[]
        deposit_data = {}
        deposit_data["FD_Number"] = deposit.id
        deposit_data["Name"] = deposit.Name
        deposit_data["Email"] = deposit.Email
        deposit_data["Age"] = deposit.Age
        deposit_data["DOB"] = deposit.DOB
        deposit_data["BankName"] = deposit.BankName
        output.append(deposit_data)
        return render_template("update.html", outputs=output)

    else:
        deposit = Deposits.query.filter_by(id=FD_Number).first()
        amount = request.form.get("amount")
        interest = request.form.get("interest")
        maturity = request.form.get("maturity")

        deposit.Amount = amount
        deposit.Interest = interest
        deposit.Maturity = maturity
        db.session.commit()

        return redirect(url_for('main.reports'))


@main.route("/delete/<int:FD_Number>")
@login_required
def delete(FD_Number):
    deposit = Deposits.query.filter_by(id=FD_Number).first()
    db.session.delete(deposit)
    db.session.commit()
    return redirect(url_for("main.reports"))


@main.route("/mydeposits")
@login_required
def mydeposits():
    deposits= Deposits.query.filter_by(Email=current_user.Email).all()

    if deposits:

        output = []
        for deposit in deposits:
            deposit_data = {}
            deposit_data["FD_Number"] = deposit.id
            deposit_data["Name"] = deposit.Name
            deposit_data["Email"] = deposit.Email
            deposit_data["Age"] = deposit.Age
            deposit_data["DOB"] = deposit.DOB
            deposit_data["BankName"] = deposit.BankName
            deposit_data["Amount_Rupees"] = deposit.Amount
            deposit_data["Interest_Rupees"] = deposit.Interest
            deposit_data["Maturity_Rupees"] = deposit.Maturity
            output.append(deposit_data)

            df2 = pd.DataFrame(output)
            df2.to_csv("csvreports/mydeposits.csv", index=False)
            return render_template("mydeposits.html", outputs=output)

    else:
        flash(" No deposits found")
        return redirect(url_for('main.profile'))


    return redirect(url_for('main.mydeposits'))























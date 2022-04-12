
import pandas as pd, sqlite3,csv
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user


from .models import Users, Deposits
from . import db
main = Blueprint('main', __name__)
from datetime import datetime as dt


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

    df1 = pd.DataFrame(output)
    df1.to_csv("adminreports.csv", index=False)


    return render_template("reports.html",outputs=output)



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
            df2.to_csv("mydeposits.csv", index=False)
            return render_template("mydeposits.html", outputs=output)

    else:
        flash(" No deposits found")
        return redirect(url_for('main.profile'))


    return redirect(url_for('main.mydeposits'))





















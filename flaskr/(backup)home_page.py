from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    url_for,
    redirect,
    flash,
    jsonify,
    Flask
)
from database import db

home_page = Blueprint("home_page",__name__)

@home_page.route('/get_all_wallets',methods=['GET', 'POST'])
def get_all_wallets():

    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT WID, WName
                FROM Wallets
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchall()
        wallets = []
        for item in result:
            wid, wname = item
            wallets.append({
                "wid": wid,
                "wname": wname
            })
        cursor.close()
        return jsonify(wallets),200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@home_page.route('/get_all_ledgers',methods=['GET', 'POST'])
def get_all_ledgers():

    wallet_id = request.args.get('wallet_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT LID, LName
                FROM Ledgers
                WHERE WID = {wallet_id};
            """
        )
        result = cursor.fetchall()
        ledgers = []
        for item in result:
            lid, lname = item
            ledgers.append({
                "lid": lid,
                "lname": lname
            })
        cursor.close()
        return jsonify(ledgers),200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@home_page.route('/get_all_goals',methods=['GET', 'POST'])
def get_all_goals():

    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT GID, GName
                FROM Goals
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchall()
        goals = []
        for item in result:
            gid, gname = item
            goals.append({
                "gid": gid,
                "gname": gname
            })
        cursor.close()
        return jsonify(goals),200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")


@home_page.route("/get_my_partner_goal", methods=["GET"])
def get_my_partner_goal():
    try:
        data_id= request.args.get("data_id")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                SELECT GID
                FROM DataToGoal
                WHERE DID = {data_id}
            """
        )
        gid = cursor.fetchall()
        return jsonify(gid), 200
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")

@home_page.route("/get_my_partner_ledger", methods=["GET"])
def get_my_partner_ledger():
    try:
        data_id= request.args.get("data_id")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                SELECT LID
                FROM DataToLedger
                WHERE DID = {data_id}
            """
        )
        lid = cursor.fetchall()
        return jsonify(lid), 200
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")
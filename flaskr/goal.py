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


goal = Blueprint("goal", __name__)

@goal.route("/<int:user_id>", methods=["GET", "POST"])
def goal_home(user_id):

    cursor = db.connection.cursor()

    # 預設：不做任何查詢，這兩個列表為 None
    my_goals_data = None
    group_goals_data = None

    if request.method == "POST":
        action = request.form.get("action")

        # -----------------------------
        # (1) Create Goal
        # -----------------------------
        if action == "create_goal":
            fat_val = request.form.get("fat")
            protein_val = request.form.get("protein")
            starch_val = request.form.get("starch")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            
            # 基本檢查
            if not (fat_val and protein_val and starch_val and start_date and end_date):
                flash("請完整輸入目標值、開始/結束日期！", "warning")
            else:
                try:
                    # 轉成數字類型或做更嚴謹的驗證
                    fat_val = float(fat_val)
                    protein_val = float(protein_val)
                    starch_val = float(starch_val)

                    sql_insert_goal = """
                        INSERT INTO `USER_GOAL` (UID, Fat, Protein, Starch, S_DATE, E_DATE)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql_insert_goal, (
                        user_id, fat_val, protein_val, starch_val, start_date, end_date
                    ))
                    db.connection.commit()

                    flash("目標新增成功！", "success")
                except Exception as e:
                    print(f"Error creating goal: {e}")
                    db.connection.rollback()
                    abort(500, "Error creating goal.")

        # -----------------------------
        # (2) My Goal
        # -----------------------------
        elif action == "my_goal":
            try:
                sql_my_goal = """
                    SELECT
                        UG.S_DATE AS StartDate,
                        UG.E_DATE AS EndDate,
                        UG.Fat AS GoalFat, 
                        UG.Protein AS GoalProtein,
                        UG.Starch AS GoalStarch,
                        COALESCE(SUM(MF.Count * F.Fat), 0) AS ActualFat,
                        COALESCE(SUM(MF.Count * F.Protein), 0) AS ActualProtein,
                        COALESCE(SUM(MF.Count * F.Starch), 0) AS ActualStarch,

                        (UG.Fat * 9 + UG.Protein * 4 + UG.Starch * 4) AS ExpectedCalories,  -- 預期大卡
                        
                        (COALESCE(SUM(MF.Count * F.Fat), 0) * 9 + 
                        COALESCE(SUM(MF.Count * F.Protein), 0) * 4 + 
                        COALESCE(SUM(MF.Count * F.Starch), 0) * 4) AS ActualCalories  -- 實際大卡

                    FROM USER_GOAL UG

                    LEFT JOIN MEAL M ON UG.UID = M.UID AND M.Dates BETWEEN UG.S_DATE AND UG.E_DATE
                    LEFT JOIN MEAL_FOOD MF ON M.UID = MF.UID AND M.MealID = MF.MealID
                    LEFT JOIN FOOD F ON MF.FoodID = F.FoodID

                    WHERE UG.UID = %s  

                    GROUP BY 
                        UG.U_GoalID,
                        UG.S_DATE,
                        UG.E_DATE,
                        UG.Fat,
                        UG.Protein,
                        UG.Starch;


                """

                cursor.execute(sql_my_goal, (user_id,))
                my_goals_data = cursor.fetchall()  # 取所有紀錄
                if not my_goals_data:
                    flash("目前查無任何目標或尚未有用餐紀錄。", "info")
            except Exception as e:
                print(f"Error fetching my goal: {e}")
                db.connection.rollback()
                abort(500, "Error fetching my goal data.")

        # -----------------------------
        # (3) Group Goal
        # -----------------------------
        elif action == "group_goal":
            sql_group_goal = """
                SELECT 
                    U.ID,
                    U.UName,
                    U.GENDER,
                    U.AGE,
                    U.HEIGHT,
                    U.WEIGHT,
                    UG.Fat      AS Goal_Fat,
                    UG.Protein  AS Goal_Protein,
                    UG.Starch   AS Goal_Starch,
                    UG.S_DATE   AS Goal_StartDate,
                    UG.E_DATE   AS Goal_EndDate
                FROM USERS U
                LEFT JOIN USER_GOAL UG ON U.ID = UG.UID
                WHERE U.ID IN (
                    -- 取出「成員」
                    SELECT GM.Members
                    FROM GROUP_MEMBER GM
                    WHERE GM.M_GroupID IN (
                        -- 找出當前使用者所屬之所有群組ID
                        SELECT M_GroupID
                        FROM GROUP_MEMBER
                        WHERE Members = %s
                        UNION
                        SELECT GroupID
                        FROM GROUP_LEADER
                        WHERE Leader = %s
                    )
                    UNION
 
                    SELECT GL.Leader
                    FROM GROUP_LEADER GL
                    WHERE GL.GroupID IN (
                        SELECT M_GroupID
                        FROM GROUP_MEMBER
                        WHERE Members = %s
                        UNION
                        SELECT GroupID
                        FROM GROUP_LEADER
                        WHERE Leader = %s
                    )
                )
            """
            try:
                cursor.execute(sql_group_goal, (user_id, user_id, user_id, user_id))
                group_goals_data = cursor.fetchall()
                if not group_goals_data:
                    flash("您尚未加入任何群組或群組成員尚未設定目標。", "info")
            except Exception as e:
                print(f"Error fetching group goal: {e}")
                db.connection.rollback()
                abort(500, "Error fetching group goal data.")

    cursor.close()

    return render_template(
        "goal_home.html",
        user_id=user_id,
        my_goals_data=my_goals_data,
        group_goals_data=group_goals_data
    )

from flask import Blueprint, request, abort, jsonify
from flask import Blueprint, request, abort, jsonify, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from database import db  # 確保 `db` 已正確實現連線池
from flask import render_template
import datetime

meal = Blueprint("meal", __name__)

@meal.route('/add_meal/<int:user_id>', methods=['GET', 'POST'])
def add_meal(user_id):
    
    
    cursor = db.connection.cursor()
    cursor.execute("SELECT FoodID, FName FROM FOOD;")
    food_options = cursor.fetchall()  # 取得所有食物的 ID & 名稱
    print("🔹 food_options (直接查詢結果):", food_options)  # 印出 SQL 結果
    
    
    if request.method == 'POST':
        action = request.form.get("action")

    #   **(A) 新增餐點**
        if action == "add_meal":
            try:
                meal_date = request.form['meal_date']
                meal_time = request.form['meal_time']  # 時間
                meal_category = request.form['meal_category']
                food_name = request.form['food_name']  # 用戶輸入的食物名稱
                food_count = int(request.form['food_count'])  # 食物數量

                # **確保輸入完整**
                if not (meal_date and meal_category and food_name and food_count > 0):
                    flash("請輸入完整的餐點資訊！", "warning")
                    return redirect(url_for('meal.add_meal', user_id=user_id))

                # **(1) 獲取新的 MealID**
                cursor.execute("SELECT COALESCE(MAX(MealID), 0) + 1 FROM MEAL WHERE UID = %s;", (user_id,))
                new_meal_id = cursor.fetchone()[0]

                # **(2) 插入 MEAL 表**
                cursor.execute("""
                INSERT INTO MEAL (MealID, UID, Dates, Times, Category)VALUES (%s, %s, %s, %s, %s);
            """, (new_meal_id, user_id, meal_date, meal_time, meal_category))

                # **(3) 檢查食物是否存在**
                cursor.execute("SELECT FoodID FROM FOOD WHERE FName = %s;", (food_name,))
                food = cursor.fetchone()

                if food:
                    food_id = food[0]
                else:
                    # **(4) 獲取新的 FoodID**
                    cursor.execute("SELECT COALESCE(MAX(FoodID), 0) + 1 FROM FOOD;")
                    food_id = cursor.fetchone()[0]

                    # **(5) 插入 FOOD 表**
                    cursor.execute(
                        "INSERT INTO FOOD (FoodID, FName) VALUES (%s, %s);",
                        (food_id, food_name)
                    )

                # **(6) 插入 MEAL_FOOD 表**
                cursor.execute(
                    "INSERT INTO MEAL_FOOD (FoodID, MealID, UID, Count) VALUES (%s, %s, %s, %s);",
                    (food_id, new_meal_id, user_id, food_count)
                )

                db.connection.commit()
                flash("Meal & Food added successfully!", "success")
                return redirect(url_for('meal.query', user_id=user_id))

            except Exception as e:
                db.connection.rollback()
                abort(500, f"❌ Error: {e}")

        # **(B) 新增食物**
        elif action == "add_food":
            try:
                food_name = request.form['food_name']
                fat = float(request.form['fat'])
                protein = float(request.form['protein'])
                starch = float(request.form['starch'])
                calories = float(request.form['calories'])

                if not food_name:
                    #flash("請輸入食物名稱！", "warning")
                    return redirect(url_for('meal.add_meal', user_id=user_id))

                # **(1) 確保食物不重複**
                cursor.execute("SELECT FoodID FROM FOOD WHERE FName = %s;", (food_name,))
                existing_food = cursor.fetchone()

                if existing_food:
                    flash("此食物已存在！", "info")
                else:
                    # **(2) 獲取新的 FoodID**
                    cursor.execute("SELECT COALESCE(MAX(FoodID), 0) + 1 FROM FOOD;")
                    new_food_id = cursor.fetchone()[0]

                    # **(3) 插入 FOOD 表**
                    cursor.execute(
                        "INSERT INTO FOOD (FoodID, FName, Fat, Protein, Starch, Calories) VALUES (%s, %s, %s, %s, %s, %s);",
                        (new_food_id, food_name, fat, protein, starch, calories)
                    )

                    db.connection.commit()
                    flash("Food added successfully!", "success")

                return redirect(url_for('meal.add_meal', user_id=user_id))

            except Exception as e:
                db.connection.rollback()
                abort(500, f"❌ Error: {e}")

    
    return render_template('add_meal.html', user_id=user_id, food_options=food_options)


@meal.route('/query/<int:user_id>', methods=['GET'])
def query(user_id):
    cursor = db.connection.cursor()
    try:
        # 查詢最近 100 天的餐點
        cursor.execute(
            """
            SELECT 
                M.MealID, M.Dates, M.Times, M.Category, 
                F.FName, F.Fat, F.Protein, F.Starch, F.Calories, MF.Count
            FROM MEAL M
            LEFT JOIN MEAL_FOOD MF ON M.MealID = MF.MealID AND M.UID = MF.UID
            LEFT JOIN FOOD F ON MF.FoodID = F.FoodID
            WHERE 
                M.UID = %s AND M.Dates >= DATE_SUB(CURDATE(), INTERVAL 100 DAY)
            ORDER BY 
                M.Dates DESC, M.Times DESC;
            """, (user_id,)
        )
        result = cursor.fetchall()

        # 整理資料：以 MealID 為 key，將相同 MealID 的食物放進同一個 meal
        meals = {}
        for row in result:
            meal_id = row[0]
            if meal_id not in meals:
                meals[meal_id] = {
                    "Date": row[1].strftime('%Y-%m-%d'),
                    "Time": str(row[2]),  # 轉換 timedelta
                    "MealCategory": row[3],
                    "Foods": []
                }
            
            # 加入食物資訊
            if row[4]:  # 避免 NULL 值
                meals[meal_id]["Foods"].append({
                    "Name": row[4],
                    "Fat": row[5],
                    "Protein": row[6],
                    "Starch": row[7],
                    "Calories": row[8],
                    "Count": row[9]
                })

        cursor.close()
        return render_template('meal_info.html', user_id=user_id, meals=meals)



    except Exception as e:
        db.connection.rollback()
        cursor.close()
        return jsonify({"status": "error", "message": str(e)})
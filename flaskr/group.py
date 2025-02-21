from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from database import db

group = Blueprint("group", __name__)

@group.route("/<int:user_id>", methods=["GET", "POST"])
def group_home(user_id):

    cursor = db.connection.cursor()
    
    # 預設 (GET) 先載入所有群組名稱，給 "Join Group" 那段用 (下拉選單)
    all_groups = []
    try:
        cursor.execute("SELECT GName FROM GROUP_LEADER;")
        all_groups = cursor.fetchall()  # 回傳 [(群組名稱,), (群組名稱,), ...]
    except Exception as e:
        print(f"Error fetching all group names: {e}")
        db.connection.rollback()
        abort(500, "Error loading group list.")
    
    # my_groups 用來儲存「我的群組」查詢結果；初次 GET 時可為 None
    my_groups = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # ---------------------------
        # 1) 查詢 "My Group"
        # ---------------------------
        if action == "my_group":
            try:
                sql_my_group = """
                SELECT GL.GroupID, GL.GName, 'Leader' AS Role
                FROM `GROUP_LEADER` GL
                WHERE GL.Leader = %s
                UNION
                SELECT GL.GroupID, GL.GName, 'Member' AS Role
                FROM `GROUP_MEMBER` GM
                JOIN `GROUP_LEADER` GL ON GM.M_GroupID = GL.GroupID
                WHERE GM.Members = %s
                """
                cursor.execute(sql_my_group, (user_id, user_id))
                my_groups = cursor.fetchall()  # [(GroupID, GName, Role), (...), ...]
                
                
            except Exception as e:
                print(f"Error fetching my groups: {e}")
                db.connection.rollback()
                abort(500, "Error fetching my group data.")
        
        # ---------------------------
        # 2) 加入 "Join Group"
        # ---------------------------
        elif action == "join_group":
            group_name = request.form.get("group_name")  # 下拉式選單的值
            try:
                sql_join = """
                    INSERT INTO `GROUP_MEMBER` (M_GroupID, Members)
                    SELECT GL.GroupID, %s
                    FROM `GROUP_LEADER` GL
                    WHERE GL.GName = %s 
                      -- 確認該用戶尚未在此群組
                      AND NOT EXISTS (
                          SELECT 1
                          FROM `GROUP_MEMBER` GM 
                          WHERE GM.Members   = %s
                            AND GM.M_GroupID = GL.GroupID

                      )
                      AND NOT EXISTS (
                          SELECT 1
                          WHERE GL.Leader = %s AND GL.GName = %s

                      );
                      
                """
                cursor.execute(sql_join, (user_id, group_name, user_id, user_id, group_name))
                db.connection.commit()
                    
                 
            except Exception as e:
                print(f"Error joining group: {e}")
                db.connection.rollback()
                abort(500, "Error joining group.")
        
        # ---------------------------
        # 3) 建立 "Create Group"
        # ---------------------------
        elif action == "create_group":
            group_name = request.form.get("group_name")
            if not group_name:
                flash("請輸入想建立的群組名稱！", "warning")
            else:
                try:
                    sql_create = """
                        INSERT INTO `GROUP_LEADER` (Leader, GName)
                        SELECT %s, %s
                        WHERE NOT EXISTS (
                            SELECT 1 FROM `GROUP_LEADER` 
                            WHERE `GName` = %s 
                        );
                    """
                    cursor.execute(sql_create, (user_id, group_name, group_name))
                    db.connection.commit()
                    
                except Exception as e:
                    print(f"Error creating group: {e}")
                    db.connection.rollback()
                    abort(500, "Error creating group.")
        # ---------------------------
        # 4) 加入 "Delete Group"
        # ---------------------------
        elif action == "delete_group":
            group_name = request.form.get("group_name")     
            try:
                delete_query = """
                    DELETE gl
                    FROM `GROUP_LEADER` gl
                    INNER JOIN `GROUP_LEADER` sub ON gl.GroupID  = sub.GroupID
                    WHERE sub.Leader  = %s
                    AND sub.GName  = %s ;
                """
                cursor.execute( delete_query, (user_id,group_name))
                db.connection.commit()
                
            except Exception as e:
                print(f"Error fetching my groups: {e}")
                db.connection.rollback()
                abort(500, "Error fetching my group data.")
        # ---------------------------
        # 5) 加入 "Exit Group"
        # ---------------------------
        elif action == "exit_group":    
            group_name = request.form.get("group_name")     
            try:
                exit_query = """
                    DELETE gm
                    FROM `GROUP_MEMBER` gm
                    INNER JOIN `GROUP_LEADER` gl ON gm.M_GroupID = gl.GroupID
                    WHERE gm.Members = %s
                    AND gl.GName= %s;

                """
                cursor.execute(exit_query, (user_id,group_name))
                db.connection.commit()
                
            except Exception as e:
                print(f"Error fetching my groups: {e}")
                db.connection.rollback()
                abort(500, "Error fetching my group data.")
    cursor.close()
    # 回到 group.html，並把 my_groups, all_groups 帶進模板
    return render_template(
        "group_home.html",
        user_id=user_id,
        my_groups=my_groups,     # 可能是 None 或 查詢結果
        all_groups=all_groups    # 供下拉式選單使用
    )

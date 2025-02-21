# DBMS Final:　Platepal

# 專案說明

PLATEPAL 是一個方便使用者紀錄飲食和營養素攝取的平台，系統能根據使用者自行紀錄之飲食內容，自動統整熱量與營養素資訊。除了個人飲食追蹤功能，PLATEPAL 還具備目標與小組功能，讓使用者不僅能自我監督，還能與他人一起互相激勵，達成共同的飲食與健康目標。此系統適合希望改善健康狀況或達成特定目標（如減重、增肌或維持健康）之使用者。

# **Database Schema**

The database contains the following tables:

### FOOD

- **`FoodID`**: Integer, Primary Key
- **`Fat`**: float
- **`Protein`**: float
- **`Starch`**: float
- **`Calories`**: float
- **`FName`**: Text

### USERS

- **`ID`**: Integer, Not Null, Primary Key
- **`UName`**: Text, Not Null
- **`Gender`**: Text(M, F)
- **`Age`**: Integer, Check (Age >= 0)
- **`Height`**: float
- **`Weight`**: float
- **`Account`**: Text
- **`Password`**: int
- **`Activity_level`**: int


### USER_GOAL

- **`U_GoalID`**: Integer, Primary Key
- **`UID`**: Integer, Foreign Key (references USERS(ID)), Not Null
- **`Fat`**: float
- **`Protein`**: float
- **`Starch`**: float
- **`S_DATE`**: date
- **`E_DATE`**: date

### MEAL 

- **`MealID`**: Integer, Primary Key
- **`UID`**: Integer, Primary Key, Foreign Key (references USERS(ID))
- **`Dates`**: date
- **`Times`**: Time
- **`Category`**: Text

### MEAL_FOOD

- **`FoodID`**: Integer, Primary Key, Foreign Key (references FOOD (FoodID))
- **`MealID`**: Integer, Primary Key, Foreign Key (references MEAL (UID, MealID))
- **`UID`**: Integer, Primary Key, Foreign Key (references MEAL (UID, MealID))
- **`Count`**: Integer

### GROUP_LEADER

- **`GroupID`**: Integer, Primary Key
- **`Leader`**: Integer, Primary Key, Foreign Key (references USERS(ID))
- **`GName`**: Text

### GROUP_MEMBER

- **`M_GroupID`**: Integer, Primary Key, Foreign Key (references GROUP_LEADER(Group_ID))
- **`Members`**: Integer, Primary Key, Foreign Key (references USERS(ID))


# **Backend Features**

### **Management**

- **Check User's Information**: Check if a user already exists or update it.
- **Add Meal**: Add a new meal to the databases.
- **Join Group**: Join a new group to cheeck the member. 
- **Set goal**: Someone can set their goal and check the goal in joined groups.

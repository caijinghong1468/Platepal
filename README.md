# Platepal

`PLATEPAL` is a user-friendly platform that automatically tracks and aggregates calorie and nutrient data from logged meals, supports personal goals, and fosters group collaboration for weight loss, muscle gain, or overall wellness.
## System Architecture  
<img src="/System Architecture.png" alt=" " />  

## ER-Model
<img src="/ER-model.png" alt=" " />  

## Relational Schema
<img src="/relational schema.png" alt=" " />  

## Database Schema

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


# System Features
**1. Personal Features:**  
-  Users can create, update, and delete their personal data (including account information and personal details).  
-  Users can independently add, update, and delete their meal records (including meal content and time).  

**2. Goal Features:**  
-  Users can set, update, and delete their dietary goals (including goal duration and nutritional targets).  
-  The system automatically tracks actual dietary data to help users assess whether they have met their goals.  

**3. Group Features:**  
-  Users can create, join, and leave friend groups. Group leaders have the authority to delete groups.  
-  Users can review their own and group members’ goal progress and meal records.  


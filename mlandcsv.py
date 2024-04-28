import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import datetime

# Load the dataset from CSV
df = pd.read_csv("C:\\Users\\Porshia Joan\\OneDrive\\Desktop\\yolov8peoplecounter-main\\data.csv")

# Preprocessing
df["Time"] = df["Time"].apply(lambda x: int(x.split(".")[0].split(":")[0]))  # Extract hour from time
df["Day"] = df["Day"].replace({"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7})  # Map days of the week to numerical values

# Split features and target variable
X = df[["Time", "Day"]]
y = df["Volume"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the decision tree regression model with hyperparameter tuning
model = DecisionTreeRegressor(max_depth=5, min_samples_split=5, min_samples_leaf=2)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)


# Get current time and day
current_time = datetime.datetime.now().hour
current_day = datetime.datetime.now().weekday()  # Monday is 0 and Sunday is 6

predicted_volume = model.predict([[current_time, current_day]])

print("Predicted volume for:", predicted_volume)

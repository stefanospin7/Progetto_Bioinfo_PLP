
import pandas as pd
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import plotly.graph_objects as go

from datetime import date as dt
data = pd.read_csv('owid-dataset.csv')
data = data[data["location"] == "World"]
print(data.columns)
data = data.fillna(0).replace(np.inf, 0)




#data['diff_tamponi'] = data['tamponi'].diff()
dates = data['date']
date_format = [pd.to_datetime(d) for d in dates]





import numpy as np
from sklearn import linear_model
# prepare the lists for the model
X = date_format
y = data['new_cases'].tolist()[1:]

oggi = date.today() - datetime.timedelta(days=1)

# date format is not suitable for modeling, let's transform the date into incrementals number starting from April 1st
starting_date = 37  # April 1st is the 37th day of the series
day_numbers = []
for i in range(1, len(X)):
    day_numbers.append([i])
X = day_numbers
# # let's train our model only with data after the peak
X = X[starting_date:]
y = y[starting_date:]
# Instantiate Linear Regression
linear_regr = linear_model.LinearRegression()



# Train the model using the training sets
linear_regr.fit(X, y)
print ("Linear Regression Model Score: %s" % (linear_regr.score(X, y)))
# Predict future trend
from sklearn.metrics import max_error
import math
y_pred = linear_regr.predict(X)
error = max_error(y, y_pred)
X_test = []
future_days = 55
for i in range(starting_date, starting_date + future_days):
    X_test.append([i])
y_pred_linear = linear_regr.predict(X_test)

#for i in range(starting_date, starting_date + future_days):
 #   X_test.append([i])
y_pred_linear = linear_regr.predict(X_test)



y_pred_max = []
y_pred_min = []
for i in range(0, len(y_pred_linear)):
    y_pred_max.append(y_pred_linear[i] + error)
    y_pred_min.append(y_pred_linear[i] - error)



print(y_pred_max)
print(y_pred_min)
print(y_pred_linear)
print(X_test)


new_df = pd.DataFrame(list(zip(X_test,y_pred_max,y_pred_min,y_pred_linear)),
               columns =['indice', 'massimo',"minimo","predictions"])



nuovo_indice = []
date_indicizzate = []



date_time_str = "2020-04-01"

date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')

#print(date_time_obj)


for i in range(0, len(new_df.indice)):
    nuovo_indice.append(new_df.indice[i][0])
    date_indicizzate.append(date_time_obj+ timedelta(days=i)

)

new_df["indice"]=date_indicizzate


print(new_df.tail())
print(new_df.dtypes)



fig = go.Figure(
            go.Bar(hoverinfo='skip',
                    x=new_df.indice,
                    y=new_df["predictions"]
                   )
            )




fig.show()



#print(new_df.indice[0])


"""

# convert date of the epidemic peak into datetime format
from datetime import datetime, timedelta
date_zero = datetime.strptime(data['date'][starting_date], '%Y-%m-%dT%H:%M:%S')
#date_zero = datetime.strptime(data['date'][starting_date], '%Y-%m-%d')
# creating x_ticks for making the plot more appealing
date_prev = []
x_ticks = []
step = 5
data_curr = date_zero
x_current = starting_date
n = int(future_days / step)
for i in range(0, n):
    date_prev.append(str(data_curr.day) + "/" + str(data_curr.month))
    x_ticks.append(x_current)
    data_curr = data_curr + timedelta(days=step)
    x_current = x_current + step

# plot known data
plt.grid()
plt.scatter(X, y)
# plot linear regression prediction
plt.plot(X_test, y_pred_linear, color='green', linewidth=2)
# plot maximum error
plt.plot(X_test, y_pred_max, color='red', linewidth=1, linestyle='dashed')
#plot minimum error
plt.plot(X_test, y_pred_min, color='red', linewidth=1, linestyle='dashed')
plt.xlabel('Days')
plt.xlim(starting_date, starting_date + future_days)
plt.xticks(x_ticks, date_prev)
plt.ylabel('new_cases')
plt.yscale("log")
plt.savefig("prediction.png")
plt.show()

data = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
zone1_df = data[data.denominazione_regione.isin(['Piemonte','Emilia-Romagna','Veneto','Lombardia'])]
zone1_df['deceduti'].sum()
print("Zone 1 accounts for %s percent of the total deaths" % (round(zone1_df['deceduti'].sum() / data['deceduti'].sum() * 100,2)))

"""

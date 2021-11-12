import pandas as pd
import numpy as np
import investpy
import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge
import plotly.express as px

today = datetime.date.today()
today = today.strftime("%d/%m/20%y")

# Busco la info
btc = investpy.get_crypto_historical_data(crypto='bitcoin',
                                           from_date='01/01/2019',
                                           to_date=today,
                                           order='ascending',
                                           interval='Daily')


# Limpio la info
btc = btc.reset_index()
btc.Date = pd.to_datetime(btc.Date)
btc = btc.drop(columns='Currency')

# Creo una variable que dice que tan larga es la tabla
btc_long = len(btc)
    
# agrega una columna con el valor promedio de BTC en el día
avg_price = []

for x in range(len(btc)):
    y= (btc.Open[x]+btc.Close[x])/2
    avg_price.append(y)

btc['Price']= avg_price

# Agrega la columna de target (el precio al otro dia)
def trading_window(data):
    n=1
    data['Target'] = data[['Price']].shift(-n)
    return data

btc = trading_window(btc)

# Paso la info a un numpy array con valores entre 0 y 1
sc = MinMaxScaler(feature_range = (0, 1))
btc_scaled = sc.fit_transform(btc.drop(columns = ['Date']))

# Defino input y output
X = btc_scaled[:,:-1]
y = btc_scaled[:,-1:]

# Le saco el último día
split = int(len(X)-1)

# Divido en entrenamiento y testeo
X_train = X[:split]
y_train = y[:split]
X_test = X[split:]
y_test = y[split:]

# Defino y corro el modelo de regresión
regression_model = Ridge(alpha=0.5)
regression_model.fit(X_train, y_train)

# Predigo los precios para toda la base
predicted_prices = regression_model.predict(X)

# Hago una lista con los valores desescalados
max = btc.Target.max()
min = btc.Target.min()
Prediction_unscaled = []
for i in predicted_prices:
    y = i[0]
    y = (y*(max-min))+min
    Prediction_unscaled.append(y)

# Agrego los datos a la planilla
btc['Predicted'] = Prediction_unscaled

# Muestro los resultados
print('Today BTC closed at {} and predicted to be {} tomorrow'.format(int(btc.Close[btc_long-1]), int(btc.Predicted[btc_long-1])))

if btc.Predicted[btc_long-1] > btc.Close[btc_long-1]:
    print('GO Long')
else: print('GO Short')

# Plot graph
last_week = btc_long -7

fig = px.line(title='Last week')
fig.add_scatter(x=btc.Date[last_week:], y=btc.Price[last_week:], name='Real Price')
fig.add_scatter(x=btc.Date[last_week:], y=btc.Predicted.shift(1)[last_week:], name='Prediction')
fig.show()
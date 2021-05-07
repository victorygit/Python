from sklearn.datasets import load_boston
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

X= np.array([1,2,3,4,5,6,7,8,9,10])
Y = 3*X*X*X + 5
plt.plot(X,Y)
plt.show()

# Move to dataframe

for p in range(1,10):
    print ('value P is ' + str(p))
    df_data = pd.DataFrame(X, columns = ['Input'])
    poly = PolynomialFeatures(p)
    X_transformed = poly.fit_transform(df_data)
    df_data_transformed = pd.DataFrame(X_transformed)
    df_target = pd.DataFrame(Y, columns = ['Target'])
    print ('---------- print data frame -----------------')
    print(df_data_transformed.head())
    print(df_target.head())

    # Liner Model
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    X_train, X_test, Y_train, Y_test = train_test_split(X_transformed,Y,test_size=0.2, random_state=0)
    #user Data frame
    #X_train, X_test, Y_train, Y_test = train_test_split(df_data_transformed, df_target, test_size=0.2, random_state=0)
    model.fit(X_train,Y_train)
    print ('Model Coef and Intercept')
    print(model.intercept_)
    print(model.coef_)
    y_predict = model.predict(df_data_transformed)
    print (df_data.head(10))
    print(y_predict)
    # Print the score
    from sklearn.metrics import mean_squared_error
    cur_score = mean_squared_error(Y, y_predict)
    print (cur_score)
    if  cur_score < 0.0005:
        print ('The right polymonial is ' + str(p))
        break

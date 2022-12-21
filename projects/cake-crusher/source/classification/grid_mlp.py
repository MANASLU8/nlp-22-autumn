from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from clf_exps import get_vectorized_data
from metrics import calculate_metrics


param_grid = [
        {
            'max_iter': [1000],
            'activation' : ['logistic', 'tanh', 'relu'],
            'solver' : ['sgd', 'adam'],
            'hidden_layer_sizes': [(5,),(10,),(15,)]
        }
       ]

X_train, y_train, X_test, y_test = get_vectorized_data(is_surface=True)
encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)
y_test = encoder.fit_transform(y_test)
clf = GridSearchCV(MLPClassifier(), param_grid, cv=3, scoring='accuracy')
#clf = MLPClassifier(activation='tanh', hidden_layer_sizes=(15,), max_iter=1000, solver='adam')
clf.fit(X_train, y_train)
print(clf.best_params_)
#{'activation': 'tanh', 'hidden_layer_sizes': (15,), 'max_iter': 1000, 'solver': 'adam'}
pred = clf.predict(X_test)
calculate_metrics(y_test, pred)

#{'activation': 'tanh', 'hidden_layer_sizes': (15,), 'max_iter': 1000, 'solver': 'adam'}

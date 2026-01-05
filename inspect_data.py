import pandas as pd
import traceback

try:
    train = pd.read_csv('data/train.csv')
    test = pd.read_csv('data/test.csv')
    print('train columns:', train.columns.tolist())
    print('train shape:', train.shape)
    print('test shape:', test.shape)

    label_col = None
    for c in ['activity', 'Activity']:
        if c in train.columns:
            label_col = c
            break
    if label_col is None:
        raise KeyError('No activity/Activity column found')

    X_train = train.drop(columns=[label_col])
    y_train = train[label_col]

    X_test = test.drop(columns=[label_col])
    y_test = test[label_col]

    print('X_train shape, y_train shape:', X_train.shape, y_train.shape)
    print('X_test shape, y_test shape:', X_test.shape, y_test.shape)
    print('y_train unique sample:', sorted(list(set(y_train)))[:10])
except Exception as e:
    print('ERROR')
    traceback.print_exc()

import pickle

try:
    with open('data.pickle', 'rb') as file:
        users: dict = pickle.load(file)
except FileNotFoundError:
    users: dict = {}

def save():
    with open('data.pickle', 'wb') as file:
        pickle.dump(users, file)
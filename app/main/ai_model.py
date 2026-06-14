import pickle

with open('main/trained_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

def categorize_ai(title: str):
    
    return loaded_model.predict([title])[0]
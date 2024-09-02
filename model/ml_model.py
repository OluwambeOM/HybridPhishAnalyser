import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load or define your model and vectorizer here
# For example:
vectorizer = TfidfVectorizer(max_features=300)
model = LogisticRegression()
optimal_threshold = 0.5

# Load pre-trained model and vectorizer
with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('model/optimal_threshold.pkl', 'rb') as f:
    optimal_threshold = pickle.load(f)

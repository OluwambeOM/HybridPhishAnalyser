from flask import Flask, render_template, request
import pickle
import re
import nltk
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the model and vectorizer
with open('model/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('model/vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

with open('model/optimal_threshold.pkl', 'rb') as threshold_file:
    optimal_threshold = pickle.load(threshold_file)

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Initialize lemmatizer and stop words
lemmatizer = nltk.WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words('english'))


# Function to preprocess email text
def preprocess_text(text):
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    tokens = nltk.word_tokenize(text)  # Tokenization
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]  # Lemmatization
    return ' '.join(tokens)


# Rules-based filter function
def rules_based_filter(subject, body, sender_email=None, attachment_list=None):
    phishing_score = 0

    # Phishing Keywords Check
    phishing_keywords = [
        'urgent', 'win', 'prize', 'click here', 'verify', 'account',
        'security alert', 'password', 'confirm', 'limited time',
        'free', 'offer', 'bank', 'lottery', 'reset your password',
        'suspended account', 'unauthorized access'
    ]
    for keyword in phishing_keywords:
        if keyword in subject.lower() or keyword in body.lower():
            phishing_score += 2

    # Check sender email
    if sender_email:
        suspicious_domains = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com']
        domain = sender_email.split('@')[-1]
        if domain in suspicious_domains:
            phishing_score += 2

    # Suspicious URL Check
    suspicious_urls = re.findall(r'http[s]?://[^\s]+', body)
    for url in suspicious_urls:
        if 'login' in url or 'verify' in url or 'update' in url:
            phishing_score += 3

    # Language Tone Analysis
    suspicious_phrases = [
        'act now', 'immediate action required', 'final notice',
        'free gift', 'limited offer', 'your account has been compromised',
        'click to claim', 'verify your identity'
    ]
    for phrase in suspicious_phrases:
        if phrase in body.lower():
            phishing_score += 1

    # Attachment Analysis
    if attachment_list:
        suspicious_filetypes = ['.exe', '.scr', '.bat', '.docm', '.xlsm', '.zip', '.rar']
        for attachment in attachment_list:
            if any(attachment.lower().endswith(ext) for ext in suspicious_filetypes):
                phishing_score += 2

    # Define a threshold; 
    return 1 if phishing_score >= 5 else 0

# Hybrid detection function
def hybrid_detection(subject, body, sender_email=None, attachment_list=None):
    # Apply rules-based filter
    if rules_based_filter(subject, body, sender_email, attachment_list):
        return 1  # Flag as phishing

    # Preprocess and vectorize
    processed_text = preprocess_text(subject + " " + body)
    vectorized_text = vectorizer.transform([processed_text])

    # Apply machine learning model 
    prob = model.predict_proba(vectorized_text)[:, 1]
    return (prob >= optimal_threshold).astype(int)[0]


# Flask route to handle form submission and display result
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']
        sender_email = request.form.get('sender_email')
        attachment_list = request.form.getlist('attachment_list')

        result = hybrid_detection(subject, body, sender_email, attachment_list)

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)

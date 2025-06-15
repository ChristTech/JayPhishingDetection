import pandas as pd
import numpy as np
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re

def extract_url_features(url):
    try:
        parsed = urlparse(url)
        
        # Basic URL components
        features = {
            'length': len(url),
            'domain_length': len(parsed.netloc),
            'path_length': len(parsed.path),
            'num_dots': url.count('.'),
            'num_digits': sum(c.isdigit() for c in url),
            'num_special_chars': len(re.findall(r'[^a-zA-Z0-9.]', url)),
            'has_https': int(parsed.scheme == 'https'),
            'has_params': int(len(parsed.params) > 0),
            'has_query': int(len(parsed.query) > 0),
            'num_directories': len([x for x in parsed.path.split('/') if x]),
            'has_suspicious_words': int(bool(re.search(r'login|admin|secure|account|password|bank|paypal|confirm', url.lower())))
        }
        
        return pd.Series(features)
    except:
        return pd.Series({k: 0 for k in ['length', 'domain_length', 'path_length', 'num_dots', 
                                       'num_digits', 'num_special_chars', 'has_https', 'has_params',
                                       'has_query', 'num_directories', 'has_suspicious_words']})

# Load dataset
print("Loading dataset...")
df = pd.read_csv('phishing_dataset/PhiUSIIL_Phishing_URL_Dataset.csv')

# Extract features
print("Extracting features...")
url_features = df['URL'].apply(extract_url_features)

# Create TF-IDF features
print("Creating TF-IDF features...")
tfidf = TfidfVectorizer(max_features=1000)
text_features = tfidf.fit_transform(df['URL'])

# Combine features
feature_names = url_features.columns.tolist() + tfidf.get_feature_names_out().tolist()
X = np.hstack([url_features, text_features.toarray()])

# Prepare labels
y = df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
print("Training Random Forest to evaluate feature importance...")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Evaluate features
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

# Print results
print("\n=== Top 20 Most Important Features ===")
print(feature_importance.head(20))

print("\n=== Model Performance ===")
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save important features
top_features = feature_importance[feature_importance['importance'] > 0.001]
top_features.to_csv('models/important_features.csv', index=False)

print(f"\nSaved {len(top_features)} important features to 'models/important_features.csv'")
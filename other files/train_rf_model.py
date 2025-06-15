from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import joblib
import json
from sklearn.metrics import classification_report

# Load your data
df = pd.read_csv('phishing_dataset/PhiUSIIL_Phishing_URL_Dataset.csv')

# Create feature extractor
def extract_url_features(url):
    features = {
        'length': len(url),
        'num_dots': url.count('.'),
        'num_digits': sum(c.isdigit() for c in url),
        'has_https': int(url.startswith('https')),
        'has_suspicious': int(any(word in url.lower() for word in ['login', 'secure', 'bank', 'account']))
    }
    return pd.Series(features)

# Extract features
print("Extracting features...")
url_features = df['URL'].apply(extract_url_features)

# Create TF-IDF features with limited vocabulary
tfidf = TfidfVectorizer(max_features=500)  # Reduced from 1000
text_features = tfidf.fit_transform(df['URL'])

# Combine features
feature_names = url_features.columns.tolist() + tfidf.get_feature_names_out().tolist()
X = np.hstack([url_features, text_features.toarray()])
y = df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)  # Reduced trees
rf_model.fit(X_train, y_train)

# Evaluate model
print("\n=== Model Performance ===")
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))

# Extract and save important features
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': rf_model.feature_importances_
})
importance = importance.sort_values('importance', ascending=False)
importance.to_csv('models/important_features.csv', index=False)

# Save model and vectorizer
joblib.dump(rf_model, 'models/rf_model.pkl')
joblib.dump(tfidf, 'models/rf_vectorizer.pkl')

# Extract rules (simplified version)
def extract_rules_from_rf(model, feature_names, n_rules=100):
    rules = []
    for tree in model.estimators_[:n_rules]:  # Limit number of trees
        tree_rules = []
        for feature_idx, threshold in zip(tree.tree_.feature, tree.tree_.threshold):
            if feature_idx != -2:  # Not a leaf node
                tree_rules.append({
                    'feature': feature_names[feature_idx],
                    'threshold': threshold,
                    'confidence': tree.tree_.value[0][0].max() / tree.tree_.value[0][0].sum()
                })
        if tree_rules:
            rules.append(tree_rules)
    return rules

# Save rules
rules = extract_rules_from_rf(rf_model, feature_names)
with open('models/rf_rules.json', 'w') as f:
    json.dump(rules, f, indent=2)

print("\nModel, features, and rules saved successfully!")
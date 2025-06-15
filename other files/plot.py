import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the feature importance CSV
df = pd.read_csv('models/important_features.csv')

# Sort by importance
df_sorted = df.sort_values('importance', ascending=False)

# Pie Chart
plt.figure(figsize=(10, 10))
plt.pie(df_sorted['importance'][:10], 
        labels=df_sorted['feature'][:10], 
        autopct='%1.1f%%')
plt.title('Top 10 Most Important Features for Phishing Detection')
plt.savefig('feature_importance_pie.png', dpi=300, bbox_inches='tight')
plt.close()

# Histogram
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='importance', bins=30)
plt.title('Distribution of Feature Importance Scores')
plt.xlabel('Importance Score')
plt.ylabel('Count')
plt.grid(True, alpha=0.3)
plt.savefig('feature_importance_hist.png', dpi=300, bbox_inches='tight')
plt.close()

print("Plots have been saved as 'feature_importance_pie.png' and 'feature_importance_hist.png'")
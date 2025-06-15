import pickle

def detect_phishing(link):
    # Load the model from the pickle file
    model = pickle.load(open('phishing.pkl', 'rb'))
    
    # Get prediction
    prediction = model.predict([link])
    
    return prediction[0]

# Only print if running directly
if __name__ == "__main__":
    # Test code here
    test_url = "www.goooggle.com"
    result = detect_phishing(test_url)
    print("Prediction:", [result])

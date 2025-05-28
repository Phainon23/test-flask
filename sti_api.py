import pandas as pd
from joblib import load
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load the model
model = load('decision_tree_model.joblib')

# Load dataset used during training to extract feature names
x = pd.read_csv('STI_data.csv')

# Print columns so we can debug and see the target column
print("Columns in dataset:", x.columns.tolist())

# Drop the target column to get features – update 'STI_Diagnose' to your actual target column name
try:
    feature_columns = x.drop(columns=['STI_Diagnose']).columns.tolist()
except KeyError:
    raise KeyError("Update 'STI_Diagnose' to the actual name of your label column in STI_data.csv")

print("Feature columns used for prediction:", feature_columns)

# Initialize Flask app
api = Flask(__name__)
CORS(api)  # Enables CORS globally

# Endpoint for Brain Stroke Prediction (HFP Prediction)
@api.route('/predict', methods=['POST', 'OPTIONS'])
def predict_brain_stroke():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        return '', 200

    try:
        # Ensure data is provided
        data = request.json.get('inputs')
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Convert input data to DataFrame
        input_df = pd.DataFrame(data)

        # Check if the input data has all the necessary feature columns
        missing_columns = [col for col in feature_columns if col not in input_df.columns]
        if missing_columns:
            return jsonify({"error": f"Missing columns: {', '.join(missing_columns)}"}), 400

        # Ensure the features match the ones used in training
        input_df = input_df[feature_columns]

        # Predict Brain Stroke Risk (HFP)
        probabilities = model.predict_proba(input_df)
        class_labels = model.classes_

        # Prepare the response with prediction probabilities
        response = []
        for prob in probabilities:
            prob_dict = {str(k): round(float(v) * 100, 2) for k, v in zip(class_labels, prob)}
            response.append(prob_dict)

        return jsonify({"Prediction": response})

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=5000)

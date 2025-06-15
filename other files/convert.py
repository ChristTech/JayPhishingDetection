import pickle
import json

# Load the model
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Convert the model to JSON format
def convert_to_json(model):
    trees = []
    for tree in model.estimators_:
        tree_dict = {
            'n_nodes': tree.tree_.node_count,
            'children_left': tree.tree_.children_left.tolist(),
            'children_right': tree.tree_.children_right.tolist(),
            'feature': tree.tree_.feature.tolist(),
            'threshold': tree.tree_.threshold.tolist(),
            'values': tree.tree_.value.tolist()
        }
        trees.append(tree_dict)
    
    model_json = {
        'n_estimators': len(model.estimators_),
        'trees': trees
    }
    return model_json

# Save as JSON
model_json = convert_to_json(model)
with open('random_forest_model.json', 'w') as f:
    json.dump(model_json, f)
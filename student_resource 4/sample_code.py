import os
import pandas as pd
import random  # Added import for random module

# Path to dataset folder
DATASET_FOLDER = 'dataset/'

def predictor(image_link, category_id, entity_name):
    '''
    Call your model/approach here
    '''
    # TODO: Implement your model prediction logic
    return "" if random.random() > 0.5 else "10 inch"

if __name__ == "__main__":
    # Load datasets
    test = pd.read_csv(os.path.join(DATASET_FOLDER, 'test.csv'))
    
    # Apply the predictor function
    test['prediction'] = test.apply(
        lambda row: predictor(row['image_link'], row['group_id'], row['entity_name']), axis=1
    )
    
    # Output file path
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')
    
    # Ensure the predictions follow the required format
    test[['index', 'prediction']].to_csv(output_filename, index=False)
    
    # Print the first few rows to check
    print(test.head())

import os
import random
import pandas as pd

def predictor(image_link, category_id, entity_name):
    '''
    Call your model/approach here
    '''
    # TODO: Implement your model prediction logic here
    return "" if random.random() > 0.5 else "10 inch"

if __name__ == "__main__":
    DATASET_FOLDER = 'dataset/'  # Relative path to the dataset folder

    test_file_path = os.path.join(DATASET_FOLDER, 'test.csv')
    
    # Print the path to debug
    print(f"Looking for file at: {test_file_path}")
    
    if not os.path.isfile(test_file_path):
        raise FileNotFoundError(f"The file {test_file_path} does not exist.")
    
    test = pd.read_csv(test_file_path)
    
    test['prediction'] = test.apply(
        lambda row: predictor(row['image_link'], row['group_id'], row['entity_name']), axis=1)
    
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')
    test[['index', 'prediction']].to_csv(output_filename, index=False)

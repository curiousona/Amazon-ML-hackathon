import os
import pandas as pd

def predictor(image_link, category_id, entity_name):
    '''
    Call your model/approach here
    '''
    # TODO: Implement your model prediction logic here
    # Example dummy prediction:
    return "10 inch"  # Ensure this format: "x unit"

if __name__ == "__main__":
    DATASET_FOLDER = 'dataset/'  # Adjusted path to be relative to this script
   
    test = pd.read_csv(os.path.join(DATASET_FOLDER, 'test.csv'))
   
    test['prediction'] = test.apply(
        lambda row: predictor(row['image_link'], row['group_id'], row['entity_name']), axis=1)
   
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')
    test[['index', 'prediction']].to_csv(output_filename, index=False)


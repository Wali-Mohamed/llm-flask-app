import os
import pandas as pd
from pathlib import Path
import minsearch

# print("Current Working Directory:", os.getcwd())
# project=os.getenv('Project_Path')
# base_path=Path(project)
# DATA_PATH = base_path / 'data' / 'clean_data'/ 'data_chunked_5s.csv'

base_path=Path('/app')
DATA_PATH = base_path / 'data' / 'data_chunked_5s.csv'
# Check if the file exists
if os.path.exists(DATA_PATH):
    print("File exists:", DATA_PATH)
else:
    print("File does not exist:", DATA_PATH)





def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)
    
    documents = df.to_dict(orient="records")

    index = minsearch.Index(
        text_fields=[
            
            "content",
        ],
        keyword_fields=[],
    )

    index.fit(documents)
    return index
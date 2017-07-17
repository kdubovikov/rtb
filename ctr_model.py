import pandas as pd
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def preprocess_data(df):
    df.drop(['bid_id', 
             'ipinyou_id', 
             'bidding_price', 
             'paying_price'
             ''])

def main():
    parser = argparse.ArgumentParser(description="Preprocess IPinYou RTB Dataset")
    parser.add_argument('--limit', '-l', type=int, help="limit loading to specified number of rows")
    parser.add_argument('--verbose', '-v', action='store_true', help="show percentage of data loaded")
    args = parser.parse_args()

    print("Loading data...")
    data = pd.read_hdf('clicks.hdf', 'clicks')
    print(data.dtypes)
    print(data.head())
    
    model = LogisticRegression(C=0.8)
    cross_val_score(model, data.drop(['click', 'user_agent'], axis=1), data['click'], verbose=1)

if __name__ == '__main__':
    main()

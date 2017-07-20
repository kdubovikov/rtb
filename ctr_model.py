"""Runnable script for RTB strategy evaluation"""

import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LogisticRegression
from bidding import FlatBiddingStrategy, BidSimulator, GoalBiddingStrategy, EffectiveCPCBiddingStrategy, RandomBiddingStrategy

def sample_data(df, sample_col, fraction=500):
    df_col = df[df[sample_col] == 1]
    df_nocol = df[df[sample_col] == 0]
    df_nocol_sample_rows = \
        np.random.choice(df_nocol.index,
                         size=int(len(df_col) * (fraction / 100)),
                         replace=False)
    df_nocol_sample = df_nocol.loc[df_nocol_sample_rows]
    df = pd.concat([df_col, df_nocol_sample])
    return df


def preprocess_data(df):
    result = df.copy()


    one_hot_col_names = ['ad_slot_visibility',
                         'browser',
                         'ad_exchange',
                         'device',
                         'os',
                         'region_id'
                         # 'ad_slot_id' # whoa, this one is large
                         ]

    one_hot_cols = pd.get_dummies(df[one_hot_col_names])

    result = pd.concat([result, one_hot_cols], axis=1)

    result.drop(one_hot_col_names, axis=1, inplace=True)

    # extract date features
    result['year'] = result['timestamp'].apply(lambda ts: ts.year)
    result['month'] = result['timestamp'].apply(lambda ts: ts.month)
    result['day'] = result['timestamp'].apply(lambda ts: ts.day)
    result['weekday'] = result['timestamp'].apply(lambda ts: ts.weekday)

    # ad_slot has only one value,
    # and user agent and timestamp were parsed before
    result.drop(['user_agent',
                 'ad_slot', 'ad_slot_id', 'timestamp'], axis=1, inplace=True)

    return result


def main():
    parser = \
        argparse.ArgumentParser(description="Preprocess IPinYou RTB Dataset")

    parser.add_argument('--verbose',
                        '-v',
                        action='store_true',
                        help="show percentage of data loaded")

    args = parser.parse_args()

    print("Loading data...")

    data = pd.read_hdf('clicks.hdf', 'clicks')
    data_preproc = sample_data(data, 'click')
    data_preproc = preprocess_data(data_preproc)
    data_preproc.drop(data_preproc.select_dtypes(include=['object']).columns,
                      axis=1,

                      inplace=True) # drop all string columns

    x = data_preproc.drop(['click', 'paying_price'], axis=1)
    y = data_preproc['click']

    x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                        stratify=y,
                                                        test_size=0.33)

    ctr_model = LogisticRegression(C=0.01, class_weight='balanced')
    scores = cross_val_score(ctr_model,
                             x_train,
                             y_train,
                             scoring='roc_auc',
                             cv=7, verbose=3)

    print("Mean CV score: %f" % np.mean(scores))

    ctr_model.fit(x, y)
    bid_simulators = [BidSimulator(data_preproc, FlatBiddingStrategy(80)),
                      BidSimulator(data_preproc, RandomBiddingStrategy(80)),
                      BidSimulator(data_preproc, GoalBiddingStrategy(80)),
                      BidSimulator(data_preproc, EffectiveCPCBiddingStrategy(data_preproc))] # LEAK HERE! split data_preproc

    for bid_simulator in bid_simulators:
        print(bid_simulator)
        stats = bid_simulator.run(ctr_model)
        print(stats)
        print(BidSimulator.metrics_report(*stats))

if __name__ == '__main__':
    main()




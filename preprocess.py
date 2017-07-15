import pandas as pd
import argparse
from data_reader import ImpressionsReader, ClicksReader


def main():
    parser = argparse.ArgumentParser(description="Preprocess IPinYou RTB Dataset")
    parser.add_argument('--limit', '-l', type=int, help="limit loading to specified number of rows")
    parser.add_argument('--verbose', '-v', action='store_true', help="show percentage of data loaded")
    args = parser.parse_args()

    print("Loading data")
    imp_reader = ImpressionsReader('./data/imp.20131019.txt')
    imp_data = imp_reader.read_data(limit=args.limit, verbose=args.verbose)

    click_reader = ClicksReader('./data/clk.20131019.txt')
    click_data = click_reader.read_data()

    print("Data")
    print(imp_data)
    print(click_data)

    print("Merging...")
    click = imp_data['bid_id'].isin(click_data['bid_id'])
    print(click.sum())

    imp_data['click'] = click
    imp_data.to_hdf('clicks.hdf', 'clicks')

if __name__ == '__main__':
    main()

import pandas as pd
import argparse
import glob
from data_reader import ImpressionsReader, ClicksReader


def main():
    parser = argparse.ArgumentParser(description="Preprocess IPinYou RTB Dataset")
    parser.add_argument('--imp-glob', '-i', type=str, help="Glob expression for impression data files", dest='imp_glob')
    parser.add_argument('--click-glob', '-c', type=str, help="Glob expression for click data files", dest='click_glob')
    parser.add_argument('--output', '-o', type=str, default="clicks.hdf", help="Output filename")
    parser.add_argument('--limit', '-l', type=int, help="limit loading to specified number of rows")
    parser.add_argument('--verbose', '-v', action='store_true', help="show percentage of data loaded")
    args = parser.parse_args()

    print("Loading data")

    imp_files = glob.glob(args.imp_glob)
    click_files = glob.glob(args.click_glob)

    if len(imp_files) != len(click_files):
        raise ValueError("Number of impression and click files does not match")

    files = list(zip(imp_files, click_files))
    print("Loading %d file pairs in total" % len(files))

    for imp, click in files:
        print("Loading pair %s %s" % (imp, click))
        imp_reader = ImpressionsReader(imp)
        imp_data = imp_reader.read_data(limit=args.limit, verbose=args.verbose)

        click_reader = ClicksReader(click)
        click_data = click_reader.read_data()

        print("Loaded data")
        print("Total impressions: %d" % len(imp_data))
        print("Total clicks: %d" % len(click_data))

        print("Merging and saving to hdf %s..." % args.output)
        click = imp_data['bid_id'].isin(click_data['bid_id'])
        print("Total clicks after merge: %d" % click.sum())

        imp_data['click'] = click
        imp_data.to_hdf(args.output, 'clicks', append=True)

if __name__ == '__main__':
    main()

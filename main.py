from data_reader import ImpressionsReader, ClicksReader


def main():
    imp_reader = ImpressionsReader('./data/imp.20131019.txt')
    imp_data = imp_reader.read_data(limit=100)

    click_reader = ClicksReader('./data/clk.20131019.txt')
    click_data = click_reader.read_data()

    print(imp_data)
    print(click_data)

if __name__ == '__main__':
    main()

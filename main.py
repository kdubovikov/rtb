from data_reader import IPinYouDataReader


def main():
    reader = IPinYouDataReader('./data/imp.20131019.txt')
    data = reader.read_data(limit=100) 

    print(data)

if __name__ == '__main__':
    main()

import codecs
import csv
from datetime import datetime
import pandas as pd
from functools import reduce
from user_agents import parse

class DataReader:
    """Sequential data reader with ability to specify it's own row parsing funtion."""

    def __init__(self, data_path, row_transformers, post_processor):
        """Create data reader for IPinYou RTB dataset.

        Parameters
        ----------
        data_path : str
            Path to data file.

        row_transformers : list of func
            Functions that parse row of data and return feature array.
            Each transformer will be applied sequentially like t3(t2(t1(row))) 

        post_processor : func
            Post processing function that takes transformed data list as input
        """

        self._row_transformers = row_transformers
        self._post_processor = post_processor
        self.data_path = data_path

    def read_data(self, limit=None):
        with codecs.open(self.data_path, 'r', encoding='utf-8', errors='ignore') as data_file:
            reader = csv.reader(data_file, delimiter='\t')
            result = []

            for i, row in enumerate(reader):
                if limit is not None and i > limit:
                    break

                # fold transformers list; apply each transformer sequentially like t3(t2(t1(row))) 
                transformed_row = reduce(lambda response, func: func(response), self._row_transformers, row)
                result.append(transformed_row)

        result = self._post_processor(result)
        return result


class IPinYouDataReader(DataReader):
    """IPinYou RTB Dataset loader."""

    def __init__(self, data_path):
        super().__init__(data_path, [self._ipinyou_data_row_transformer],
                                     self._preprocess_data)

    @staticmethod
    def _ipinyou_data_row_transformer(row):
        """Load data from ipinyou dataset format.
        Expecting impression log form 2-nd or 3-rd rounds.

        Parameters
        ----------
        file_name : str
            Path to the dataset.

        limit : int
            Limit loading to first `limit` lines."""

        entry = {'bid_id': row[0],
                 'timestamp': row[1],
                 'log_type': row[2],
                 'ipinyou_id': row[3],
                 'user_agent': row[4],
                 'ip_address': row[5],
                 'region_id': row[6],
                 'city_id': row[7],
                 'ad_exchange': row[8],
                 'domain': row[9],
                 'url': row[10],
                 'anonymous_url_id': row[11],
                 'ad_slot_id': row[12],
                 'ad_slot_width': row[13],
                 'ad_slot_height': row[14],
                 'ad_slot_visibility': row[15],
                 'ad_slot': row[16],
                 'ad_slot_floor_price': row[17],
                 'creative_id': row[18],
                 'bidding_price': row[19],
                 'paying_price': row[20],
                 'key_page_url': row[21],
                 'advertiser_id': row[22],
                 'user_tags': row[23]}

        entry['user_tags'] = [int(tag) for tag in entry['user_tags'].split(
            ',')] if entry['user_tags'] != 'null' else None
        entry['timestamp'] = datetime.strptime(
            entry['timestamp'][:-3], '%Y%m%d%H%M%S')

        return entry

    @staticmethod
    def _preprocess_data(data):
        """Perform basic data preprocessing
        
        Parameters
        ----------
        data : list of dict
            Impression data log, can be loaded with :func:`load_data`

        Returns
        -------
        df : pandas.DataFrame
        """

        user_tag_col_cache = set()

        for d in data:
            # parse user agent
            user_agent = parse(d['user_agent'])
            d['os'] = user_agent.os.family
            d['browser'] = user_agent.browser.family
            d['device'] = user_agent.device.family

            # vectorize user tags (one-hot)
            tags = d['user_tags']

            if tags is not None:
                for t in tags:
                    col_name = "user_tag_%d" % t
                    user_tag_col_cache.add(col_name)

                    d[col_name] = 1
        
        df = pd.DataFrame(data)
        df.drop('user_tags', inplace=True, axis=1)
        df[list(user_tag_col_cache)] = df[list(user_tag_col_cache)].fillna(0) # fill not present tags with 0 for each user

        return df
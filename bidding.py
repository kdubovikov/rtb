"""Bidding module"""
import numpy as np

class BidSimulator:
    """Simulates given bidding strategy on a dataset"""

    def __init__(self, data, bidding_strategy):
        """Initialize bidding simulator.

        Parameters
        ----------
        data : pandas.DataFrame
            Historical data containing features for model predicti n, bidding price,
            winning price, impressions and click indicators.
            Expected column names:

        bidding_strategy : func
            Function that retuns bid given prospenity to click and data row
        """

        self._data = data
        self._bidding_strategy = bidding_strategy

    def run(self, ctr_model=None):
        """Run bidding simulator

        Parameters
        ----------
        ctr_model : sklearn-like model
            Binary classifier for click prospenity

        Returns
        -------
        bids : list
            Bids for each entry in the data"""

        total_impressions = 0
        total_ad_spend = 0
        total_clicks = 0

        for i, row in self._data.iterrows():
            if ctr_model is not None:
                prospenity = ctr_model.predict_proba(
                    row.drop(['click', 'paying_price']).values.reshape(1, -1))[0][1]
            else:
                prospenity = None

            bid = self._bidding_strategy(prospenity, row)
            
            if bid >= row['paying_price']:
                total_impressions += 1
                total_ad_spend += row['paying_price']
                if row['click']:
                    total_clicks += 1

        return total_clicks, total_impressions, total_ad_spend

    @staticmethod
    def metrics_report(total_clicks, total_impressions, total_ad_spend):
        """Generate metric let g:pymode_lint = 0u

        Returns
        -------
        cpc : float
            Cost Per Click.

        ctr : float
            Click Through Rate.

        cpm : float

            Cost Per Mille.
        """
        ctr = BidSimulator.ctr(total_clicks, total_impressions)
        cpm = BidSimulator.cpm(total_ad_spend, total_impressions)
        cpc = BidSimulator.cpc(total_ad_spend, total_clicks)

        report = "CTR:\t%.2f\nCPM:\t%.3f\nCPC:\t%.3f" % (ctr, cpm, cpc)

        return report

    @staticmethod
    def ctr(num_of_clicks, num_of_impressions):
        """Claculate Click Through Rate - frequency of clicks on ads."""
        return num_of_clicks / num_of_impressions if num_of_impressions > 0 else 0

    @staticmethod
    def cpm(total_spendings, num_of_impressions):
        """Calculate Cost Per Mille - total cost advertiser pays for 1000 impressions."""
        return total_spendings / num_of_impressions * 1000 if num_of_impressions > 0 else 0

    @staticmethod
    def cpc(total_spendings, num_of_clicks):
        """Calculate Cost Per Click"""
        return total_spendings / num_of_clicks if num_of_clicks > 0 else 0

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__,
                self._bidding_strategy.__class__.__name__)


class RandomBiddingStrategy(object):
    def __init__(self, bid):
        """Create flat bidding strategy

        Parameters
        ----------
        bid : float
            Bid value
        """
        self._bid = bid

    def __call__(self, prospenity, row):
        """Execute bidding strategy

        Parameters
        ----------
        prospenity : float
            prospenity to click
        row : dict-like
            data row with features, pricing, impression and click data

        Returns
        -------
        bid_price : float
        """

        return np.random.rand() * self._bid


class FlatBiddingStrategy():
    """Constant bid"""

    def __init__(self, bid):
        """Create flat bidding strategy

        Parameters
        ----------
        bid : float
            Bid value
        """
        self._bid = bid

    def __call__(self, prospenity, row):
        """Execute bidding strategy

        Parameters
        ----------
        prospenity : float
            prospenity to click
        row : dict-like
            data row with features, pricing, impression and click data

        Returns
        -------
        bid_price : float
        """

        return self._bid


class GoalBiddingStrategy():
    """Bid based on prospenity"""

    def __init__(self, bid):
        """Create bidding strategy

        Parameters
        ----------
        bid : float
            Bid value
        """
        self._bid = bid

    def __call__(self, prospenity, row):
        """Execute bidding strategy

        Parameters
        ----------
        prospenity : float
            prospenity to click
        row : dict-like
            data row with features, pricing, impression and click data

        Returns
        -------
        bid_price : float
        """

        return prospenity * self._bid


class EffectiveCPCBiddingStrategy(GoalBiddingStrategy):
    """Bid based on prospenity and CPC calculated from training data"""

    def __init__(self, data):
        """Create bidding strategy

        Parameters
        ----------
        data : pd.DataFrame
            Historical data
        """
        effective_cpc = data['paying_price'].sum() / data['click'].sum()
        print(effective_cpc)
        super().__init__(effective_cpc)

Real Time Bidding with Python
=============================

This is an example implementation of a real time bidding system in
python. It is not a production-grade and was created to provide clear
and structured codebase for educational purposes. This repository also
contains a microframework for testing out various bidding strategies.

`You may read a full tutorial on RTB and this project in particular
here. TBA <>`_

Dataset
-------

This project uses open IPinYou RTB dataset located at
http://data.computational-advertising.org. The main site lacks
descriptions, but they are available as papers: 

- `iPinYou Global RTB Bidding Algorithm Competition Dataset <http://contest.ipinyou.com/ipinyou-dataset.pdf>`_ 
- `iPinYou DSP Bidding Log Format <http://math.stanford.edu/~yuany/course/2013.spring/dsp_bidding_data_format.pdf>`_

Code structure
--------------

All core features are located at ``rtb`` package. ``data_reader``
module contains framework for reading data from text files and
implementations of readers for IPinYou logs ``bidding`` module
contains ``BiddingSimulator`` that allows to evaluate various bidding
strategies. Several popular strategies as well as baselines are provided
within this package too

``preprocess.py`` script is a CLI utility that can preprocess several
IPinYou files into a single HDF that can be used onwards.

``ctr_model.py`` sctipt is a CLI utility that evaluates several bidding
stategies with predictive CTR model based on logistic regression.


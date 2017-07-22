Usage
=====

1. Create conda environment using provided env file

   ::

       $ conda create -f ./conda-environment.yml
       $ source activate rtb

2. Download and extract IPinYou data. You may use logs from
   ``training2`` or ``training3``. Those folders contain extended data
   compared to ``training1``

   ::

       $ cd ./ipinyou_data_dir/training2 && bunzip2 -k clk* && bunzip2 -k imp*
       $ mv *.txt rtb_project_dir/data

3. Preprocess data. Script needs to be run from project root.

   ::

       $ python preprocess.py -h
       $ python preprocess.py -i './data/imp*' -c './data/clk*' -v

4. Evaluate bidding strategies

   ::

       $ python ctr_model.py -h
       $ python ctr_model.py


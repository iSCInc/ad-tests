# Ad Eng automation tests
Requirements:
  - python 2.7
  - phantomjs
  - FF

Workflow:
  1.  `git clone git@github.com:Wikia/ad-tests.git && cd ad-tests` to clone the repo and go to the tests folder
  2.  `pip install -r requirements.txt` to install all dependencies.
  3.  `python ad_tests.py` to run the tests.

Find screenshots and raw html files in `logs` folder on test failure.  
Find logs in Dropbox folder if you run the tests with `send-dropbox` argument:  
`python ad_tests.py send-dropbox`  
Dropbox folder: https://www.dropbox.com/sh/6ietqx6er35ag23/AAAyhzHfbUh8SRZ5V-EERtmha?dl=0

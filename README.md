# seaQuoraQuestDuplicate

Problem source:
https://www.kaggle.com/c/quora-question-pairs


1. create input files, ETL for orginal xml format docs 
./assignment4/reformat_all.sh

2. start mapreduce framework, RESTful service accept user-defined program and input through HTTP request
python -m assignment3.workers

3. submit inverted indexing tasks(under dir "seaQuoraQuestDuplicate/assignment4/mr_apps/") to mapreduce framework 
python -m assignment4.start

4. start search engine backend, including load balancer, and accept multi-words query
python -m assignment2.start 

5. start search engine frontend
python -m webapp.start


Now, you can visit http://linserv1.cims.nyu.edu:22750/ to start search.






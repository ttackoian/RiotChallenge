# RiotChallenge
Submission to Riot API Challenge

Team Member 1:
Leo Kwan, CA USA
Summoner Name: Codelyouko, NA

Team Member 2:
James Wei, CA USA
Summoner Name: AWeiOfLife, NA

Project Description:

For our project we decided to evaluate different team compositions through a decision tree. Each data point was a 124-feature vector, with each feature representing a champion, and had a 1/0 classification for win/loss.

We used the new endpoint and retrieved about 50k gameIds, or about 100k data points for our decision tree to train on. QueryGenerator.py generates a .mat file for RiotDecisionTree.py to use. This was done through scraper.py and fetcher.py through the new URF endpoint. 

WARNING: RiotDecisionTree.py takes in a tunable depth for the tree. Depending on the depth and how many data points you want to train on, it can take a while. ~6hrs for 100k data points and a depth of 125. 

Usage:

Use 
python QueryGenerator.py 
to generate a testData.mat file of comps you want to throw into the decision tree.

Use 
python DecisionTree.py (trainingData) testData.mat
to begin training. TrainingData can be an .mat design matrix file of your choice, enclosed in the repo is the zipped file of all 100k data points we used to train on.

EX:
python DecisionTree.py riotData.mat testData.mat

The results will come out as a csv file. 

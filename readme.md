# Article classification

### Objectives

This python script provides an easy way to visualize data about your friends network

### Requirements

This script uses the packages [networkx ](https://networkx.github.io/ (network visualization on python) and [community ](https://bitbucket.org/taynaud/python-louvain "community")(community detection with the louvain method).

### Getting the data

Your facebook data can be downloaded in a csv after getting the app [link givemydata](http://www.givememydata.com/ "Give My Data") like follows:

![alt text](https://github.com/charlesdurand/facebook_data/blob/master/images/facebook_instructions.png)

### Use

The class **FacebookGraph** is initialized with the path of the csv previously downloaded, and your facebook name.

The three functions **ego_plot(radius, name)**, **common_friends_plot()** and **community_plot()** enable to visualize the categorisation:

###### ego_plot(radius, name):
This enables to visualize, for a given person outside yourself, a graph of the friends to a certain degree (radius):
![alt text](https://github.com/charlesdurand/facebook_data/blob/master/images/ego_graph.png)

###### common_friends_plot():
This enables to visualize the repartition of your friends depending on the number of common friends with them:
![alt text](https://github.com/charlesdurand/facebook_data/blob/master/images/number_of_common_friends_of_friends.png)

###### common_friends_plot():
This enables to visualize your network, split by coherent groups (on the grounds of mutual relationship between members) thanks to the  package community.
Each group being split, you are asked to label each group based on some of its elements:
![alt text](https://github.com/charlesdurand/facebook_data/blob/master/images/input.png)
The output enables to visualize your friends' network in a global manner:
![alt text](https://github.com/charlesdurand/facebook_data/blob/master/images/my_facebook_network.png)

*The examples above use my own Facebook personal data (hence the low quality of the pictures for privacy reasons)*
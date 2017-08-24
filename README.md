# Climb-Bot
Climb-Bot is a Reddit bot that provides information on routes mentioned in posts on climbing-related subreddits.

Climb-Bot uses Google's search engine API as a NLP engine and for extracting route metadata.
To run the bot, you may register an API key at https://cse.google.com

Route metadata is extracted from theCrag.com; Reddit API accessed through PRAW (Python Reddit API Wrapper)

Currently in the process of implementing the fastText NLP model to assist in classification of route names:

Created a file containing all posts ever made (about 50,000 posts) to r/climbing and r/bouldering: posts.txt.
Labeled them (__label__1 for routes, __label__2 for nonroutes) as according to my current identification process.
Need to find method to relabel the posts to increase accuracy and include posts that lack a grade.
  

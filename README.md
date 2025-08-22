# TxMM_AI_Sentiment_Analysis

This project explores public perceptions of artificial intelligence (AI) by mining English-language Reddit posts and their comments. The goal is to identify discussion topics around AI on Reddit and analyze the sentiment expressed within those topics. 

The project is based on scraping relevant posts using the Reddit API (PRAW), followed by preprocessing, K-Means clustering for topic modeling, and VADER sentiment analysis for comment evaluation.

## Features

- **Data Collection:** Finds AI-related posts using broad search terms and subreddit exploration, filtering for relevance and minimum comment counts. This step is performed in `Data_Collection_private_app_info_removed.py`
- **Multistage Text Preprocessing:** Includes language filtering (at least 95% English using `langdetect`), link removal, case normalization, stopword removal, and lemmatization.
- **Topic Discovery:** Uses TF-IDF vectorization and K-Means clustering (12 clusters chosen) to group posts by thematic similarity.
- **Sentiment Analysis:** Applying NLTK’s VADER SentimentIntensityAnalyzer on comments clustered by topic to classify sentiments as positive, neutral, or negative.
- **Visualization:** Interactive t-SNE visualizations of post clusters using Plotly. Note: If they do not load, you can either load the notebook in Google Colab or re-run the notebook yourself after collecting the data.
- **Comprehensive Reporting:** Clusters are labeled with top terms and analyzed for sentiment distributions, revealing nuanced insights across AI-related domains.

## Project Structure

- `Data_Collection_private_app_info_removed.py`: Script for collecting Reddit posts and comments using PRAW with error handling and a broad search.
- `Preprocessing_and_analysis.ipynb`: Contains preprocessing pipelines, English filtering, post-clustering, Comment sorting based on cluster organization, and sentiment analysis.
- `reddit_posts24-10/`: Directory with raw post and comment text files. (Not Provided)
- `reddit_posts24-10subreddit_posts/`: Directory with raw post and comment text files collected from the list of discovered subreddits. After collection, `reddit_posts24-10/` and `reddit_posts24-10subreddit_posts/` are merged into `reddit_posts24-10/`. (Not Provided)
- `reddit_posts24-10_combined_english_cleaned_posts/`: Processed cleaned post files ready for clustering. (Not Provided)
- `reddit_posts24-10_combined_english_comments_12_clusters/`: Comments sorted into topic clusters. (Not Provided)

## Instructions
First, you must get your Reddit Application information, which you can get by following the PRAW guide here: https://praw.readthedocs.io/en/stable/getting_started/authentication.html
Afterwards, simply run the `Data_Collection_private_app_info_removed.py` file to collect your data. Finally, run the entire `Preprocessing_and_analysis.ipynb` notebook to perform the entire analysis pipeline.

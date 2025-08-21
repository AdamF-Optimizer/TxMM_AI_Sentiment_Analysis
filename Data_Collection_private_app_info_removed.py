import praw
import prawcore
import re
import time
from prawcore.exceptions import RequestException, ServerError
import os

# Reddit setup remains the same
reddit = praw.Reddit(
    client_id="Your Client ID", # TODO: Use your own Client ID
    client_secret="Your Client Secret", # TODO: Use your own Client Secret
    user_agent="Your Reddit App Name" # TODO: Use your own Reddit App Name
)

# list of primary search terms
primary_keywords = ["AI ", " AI ", "artificial intelligence", "machine learning", "deep learning", "neural network", "computer vision", "chatgpt", "gpt", "reinforcement learning",
                    "unsupervised machine learning", "supervised machine learning", "vision transformer", "convolutional neural network", "large language models",
                    "generative AI", "natural language processing", "openAI", "google AI", "microsoft AI", "explainable AI", "XAI", "AI ethics", "AI healthcare",
                    "AI jobs", "AI art", "AI work", "AI bad", "AI evil", "AI good", "AI audio", "AI visuals", "chatbot", "LLM"]

def is_relevant_post(post):
    if post.selftext != "":
        body = remove_links(post.selftext.lower())
    else: # Don't use posts that have no text content
        return False
    title = remove_links(post.title.lower())
    combined_text = f"{title} \n {body}"
    
    # # Check for exact matches of key phrases in title and text
    keywords = list(map(lambda x : x.lower(), primary_keywords))
    # Check if any of the broader keywords are present in the title or body
    if any(keyword in combined_text for keyword in keywords):
        return True

    # Check for any AI-related acronyms ocurring in the title and text
    ai_acronyms = [r"\bML\b", r"\bNLP\b", r"\bViT\b"]
    if any(re.search(acronym, combined_text) for acronym in ai_acronyms):
        return True
    
    return False

def clean_filename(title):
    title = re.sub(r'[\\/*?:"<>|]', "", title) # Remove invalid characters for windows filesystem
    title = re.sub(r'[\n\r\t]+', " ", title)  # Replace newlines and tabs with spaces
    title = title.strip(". ") # Remove leading/trailing spaces and dots
    return title[:100] # Only return the first 100 characters for the title name

def remove_links(text):
    return re.sub(r'http[s]?://\S+|www\.\S+', '', text)

def save_post_and_comments_to_file_save_subs(keyword, subreddit_set, posts_save_folder):
    saved_count = 0
    processed_count = 0
    
    try:
        for post in reddit.subreddit("all").search(keyword, limit=None):
            processed_count += 1
            
            if not is_relevant_post(post):
                continue

            post.comments.replace_more(limit=0)
            comments = post.comments.list()

            if not comments or len(comments) < 5:
                continue

            clean_title = clean_filename(post.title)
            file_name = f"{posts_save_folder}/{clean_title}.txt"

            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(f"Post Title: {post.title}\n")
                    f.write(f"Post Subreddit: {post.subreddit}\n")
                    subreddit_set.add(post.subreddit) # Save subreddit for additional searching later on
                    f.write(f"Post URL: {post.url}\n")
                    selftext = remove_links(post.selftext)
                    f.write(f"Post Body:\n{selftext}\n\n")

                    for comment in comments:
                        if comment.body == "[deleted]": # S
                            continue
                        f.write(f"From subreddit: {comment.subreddit}\n")
                        f.write(f"Comment by {comment.author}:\n")
                        postcomment = remove_links(comment.body)
                        f.write(f"{postcomment}\n\n")

                print(f"Saved post '{clean_title}' from r/{post.subreddit} to {file_name}")
                saved_count += 1
            except IOError as e:
                print(f"Error writing file {file_name}: {e}")
                continue

    except prawcore.exceptions.NotFound:
        print(f"An error occurred: URL not found.")
    except RequestException as e:
        print(f"Request exception: {str(e)}")
    except ServerError as e:
        print(f"Server error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        print(f"Processed {processed_count} posts, saved {saved_count} relevant posts.")
    
    return saved_count

save_folder = "reddit_posts24-10" # TODO: Use your own folder
os.makedirs(save_folder, exist_ok=True)
total_saved_global_search = 0
subreddit_set = set()

for keyword in primary_keywords:
    print(f"Searching across Reddit for: {keyword}")
    saved = save_post_and_comments_to_file_save_subs(keyword, subreddit_set, posts_save_folder=save_folder)
    total_saved_global_search += saved

print(f"Total posts saved: {total_saved_global_search}")


with open("posts24-10subredditset.txt", "w") as file: # TODO: Use your own file
    for item in subreddit_set:
        file.write(f"{item}\n")





################################
### FOR SUBREDDIT SEARCHING ####
################################



with open('posts24-10subredditset.txt', 'r') as file: # TODO: Use your own file
    # Read each line into a list, stripping any extra newline characters
    subreddit_list = [line.strip() for line in file]


def save_post_and_comments_to_file(keyword, subreddits, base_folder="reddit_posts"):
    saved_count = 0
    processed_count = 0
    
    try:
        for subreddit_name in subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.search(keyword, limit=None):
                processed_count += 1
                
                if not is_relevant_post(post):
                    continue

                post.comments.replace_more(limit=0)
                comments = post.comments.list()

                if not comments:
                    continue

                clean_title = clean_filename(post.title)
                file_name = f"{base_folder}/{subreddit_name}_{clean_title}.txt"

                try:
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(f"Post Title: {post.title}\n")
                        f.write(f"Post Subreddit: {post.subreddit}\n")
                        f.write(f"Post URL: {post.url}\n")
                        selftext = remove_links(post.selftext)
                        f.write(f"Post Body:\n{selftext}\n\n")
                        

                        for comment in comments:
                            if comment.body == "[deleted]":
                                continue
                            f.write(f"From subreddit: {comment.subreddit}\n")
                            f.write(f"Comment by {comment.author}:\n")
                            postcomment = remove_links(comment.body)
                            f.write(f"{postcomment}\n\n")

                    print(f"Saved post '{clean_title}' from r/{subreddit_name} to {file_name}")
                    saved_count += 1
                except IOError as e:
                    print(f"Error writing file {file_name}: {e}")
                    continue

    except prawcore.exceptions.NotFound:
        print(f"An error occurred: URL not found.")
    except RequestException as e:
        print(f"Request exception: {str(e)}")
    except ServerError as e:
        print(f"Server error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        print(f"Processed {processed_count} posts, saved {saved_count} relevant posts.")
    
    return saved_count


save_folder = "reddit_posts24-10subreddit_posts" # TODO: Use your own folder
os.makedirs(save_folder, exist_ok=True)
total_saved_subreddit_search = 0

for keyword in primary_keywords:
    print(f"Searching across specified subreddits for: {keyword}")
    saved = save_post_and_comments_to_file(keyword, list(subreddit_list), base_folder=save_folder)
    total_saved_subreddit_search += saved

print(f"Total posts saved from subreddits: {total_saved_subreddit_search}")

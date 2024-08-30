import os
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()

def search_youtube(query):
    # Set up the Google Custom Search API client
    api_key = os.getenv('GOOGLE_API_KEY')
    cx = os.getenv('GOOGLE_CX')
    
    if not api_key or not cx:
        raise ValueError("GOOGLE_API_KEY and GOOGLE_CX environment variables must be set.")
    
    service = googleapiclient.discovery.build("customsearch", "v1", developerKey=api_key)

    # Search for the given query on YouTube
    try:
        result = service.cse().list(
            q=query + " site:youtube.com",
            cx=cx,
            num=3,  # Return the top 3 results
            start=1,
            lr="lang_en",  # Search for English language results
            safe="off"
        ).execute()
    
        # Extract the video URLs from the search results
        video_urls = [item['link'] for item in result['items'] if 'youtube.com/watch' in item['link']]
        return video_urls
    
    except Exception as e:
        print(f"Error searching for YouTube videos: {e}")
        return []

# Example usage
query = "Machine Learning Tutorial"
urls = search_youtube(query)

if urls:
    print(f"Top 3 YouTube videos for '{query}':")
    for url in urls:
        print(url)
else:
    print("No YouTube videos found for the given query.")
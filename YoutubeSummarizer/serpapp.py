import requests
from dotenv import load_dotenv
import os
load_dotenv()

def search_youtube(topic):
    # Set your SerpApi API key
    api_key = os.getenv('SERPAPI_KEY')
    
    if not api_key:
        raise ValueError("SERPAPI_KEY environment variable must be set.")
    
    # Define the endpoint and parameters
    url = 'https://serpapi.com/search.json'
    params = {
        'engine': 'youtube',
        'search_query': topic,
        'api_key': api_key,
    }

    # Make the API request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        video_results = results.get('video_results', [])
        video_urls = [video['link'] for video in video_results]
        return video_urls[:2]  # Return only the top 2 results
    else:
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        return []

# # Example usage
# topic = "Machine Learning Tutorial"

def get_urls(topic):
    urls = search_youtube(topic)
    return urls

# if urls:
#     print(f"Top 3 YouTube videos for '{topic}':")
#     for url in urls:
#         print(url)
# else:
#     print("No YouTube videos found for the given topic.")
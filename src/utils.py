#json handler/env loads/web scraper
import os
import json
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup 
from groq import Groq
from googleapiclient.discovery import build
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

DEFAULT_SOURCE_NUM = 5
RELIABILITY_THRESHOLD = 0.7
MAX_SUMMARY_LENGTH = 100

groq_client = Groq(api_key=GROQ_API_KEY)
service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
cx=GOOGLE_CSE_ID

def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def web_scrap(query: str, num_results: int = 2) -> dict:
    try:
        res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=num_results).execute()

        search_results = []
        for item in res.get('items', []):
            title = item.get('title', 'No title')
            link = item.get('link', 'No link')
            snippet = item.get('snippet', 'No snippet')
            search_results.append({"title": title, "link": link, "snippet": snippet})

        if not search_results:
            return {"url": "", "content": "No results found."}

        # Select the most relevant result
        most_relevant_url = search_results[0]['link']
        # print(f"Most relevant URL: {most_relevant_url}")

        # Fetch the page content
        response = requests.get(most_relevant_url)
        if response.status_code != 200:
            return {"url": most_relevant_url, "content": f"Failed to fetch the page. Status code: {response.status_code}"}

        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()

        # Extract main content based on common content containers
        main_content = None
        content_selectors = [
            'main', 
            'article',
            'div[role="main"]',
            '.main-content',
            '#content',
            '.post-content',
            '.article-content'
        ]

        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break

        if not main_content:
            main_content = soup.find('body')

        # Extract structured content
        content = {
            'title': soup.title.string if soup.title else '',
            'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
            'paragraphs': []
        }

        if main_content:
            # Get paragraphs with actual content
            for p in main_content.find_all('p'):
                text = p.get_text(strip=True)
                if len(text) > 50:  # Filter out short snippets
                    content['paragraphs'].append(text)

        # Combine the structured content
        formatted_content = f"Title: {content['title']}\n\n"
        
        if content['headings']:
            formatted_content += "Main Topics:\n"
            formatted_content += "\n".join(f"- {h}" for h in content['headings'][:10]) + "\n\n"
        
        if content['paragraphs']:
            formatted_content += "Content:\n"
            formatted_content += "\n\n".join(content['paragraphs'][:15])  # Limit to first 10 substantial paragraphs

        # Clean up the content
        cleaned_content = formatted_content.replace('\n\n\n', '\n\n').strip()
        # print("MOST relevant information: ", cleaned_content)
        return {
            'url': most_relevant_url,
            'content': cleaned_content
        }

    except Exception as e:
        print(f"Error in web_scrap: {str(e)}")
        return {"url": "", "content": f"Error occurred: {str(e)}"}

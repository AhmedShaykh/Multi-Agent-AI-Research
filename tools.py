from langchain.tools import tool;
from tavily import TavilyClient;
from dotenv import load_dotenv;
from bs4 import BeautifulSoup;
import requests;
import os;

load_dotenv();

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"));

@tool
def web_search(query : str) -> str:

    """Search The Web For Recent & Reliable Information On A Topic. Returns Titles, URLs & Snippets."""

    results = tavily.search(query=query, max_results=5);

    out = [];

    for r in results["results"]:

        out.append(f"Title: {r["title"]}\nURL: {r["url"]}\nSnippet: {r["content"][:300]}\n");
    
    return "\n----\n".join(out);

@tool
def scrape_url(url: str) -> str:

    """Scrape & Return Clean Text Content From A Given URL For Deeper Reading."""

    try:

        res = requests.get(
            url,
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0"
            });

        soup = BeautifulSoup(res.text, "html.parser");

        for tag in soup(["script", "style", "nav", "footer"]):

            tag.decompose();

        return soup.get_text(separator=" ", strip=True)[:1500];

    except Exception as e:

        return f"Could Not Scrape URL: {str(e)}";
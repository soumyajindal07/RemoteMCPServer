from fastmcp import FastMCP
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
import os

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

mcp = FastMCP("WebSearch")

tool = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # search_depth="advanced",
    # include_domains = []
    # exclude_domains = []
)

@mcp.tool()
async def webSearch(textToSearch: str):
    """
    Get the list of details from web using Tavily tool
    """
    try:
        results = tool.invoke(textToSearch)
        # Return top 5 results as a simple list of dicts
        output = []
        for item in results[:5]:
            print(item)
            output.append({
                "title": item.get("title"),
                "link": item.get("url"),
                "content": item.get("content")
            })
        return output
    except Exception as e:
        return {"error": str(e)}
    
# Start the server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    # mcp.run()
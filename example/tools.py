import httpx
import sys
import json
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Example tools")

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    # api_key = sys.argv[1]
    load_dotenv()
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}")
        v = json.loads(response.text)
        t = round(v["main"]["temp"] - 273.15, 2)
        ft = round(v["main"]["feels_like"] - 273.15, 2)
        return "Temperature: " + str(t) + "C, feels like " + str(ft) + "C. " + v["weather"][0]["description"]

if __name__ == "__main__":
    mcp.run(transport="stdio")

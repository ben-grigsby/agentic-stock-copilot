from pydantic import BaseModel, Field
from SMA_EMA import get_momentum_status
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

df = pd.read_csv('../infra/data/raw/daily_bars.csv')

# sample user input
user_input = 'show me the momentum of nvidia in the recent 200 days'

class MomentumInput(BaseModel):
    ticker: str = Field(
        ..., 
        description="The stock ticker symbol in uppercase (e.g., 'AAPL', 'NVDA')."
    )
    window_days: int = Field(
        20, 
        description="The lookback window in days for the moving averages. Common values are 20, 50, or 200."
    )
    
def momentum_tool(ticker: str, window_days: int):
    if ticker.upper() not in df['symbol'].unique():
        return {"error": f"Sorry, we do not have the data for the stock you're looking for ({ticker})"}
    return get_momentum_status(df, ticker.upper(), window_days)

TOOLS = {
    "get_momentum_status": {
        "function": momentum_tool,
        "schema": MomentumInput,
        "description": "Analyze stock momentum using SMA and EMA"
    }
}

tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "get_momentum_status",
            "description": TOOLS["get_momentum_status"]["description"],
            "parameters": MomentumInput.model_json_schema()
        }
    }
]


load_dotenv()
# store your api key in the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)
model_id = "gemini-2.5-flash" 

tools_config = [momentum_tool] 

# Model Call
response = client.models.generate_content(
    model=model_id,
    contents=user_input,
    config=types.GenerateContentConfig(
        tools=tools_config,
        system_instruction= 
        '''
        You are a specialized Stock Market Analytics Copilot. 
        Your ONLY purpose is to analyze stock data using your deterministic tools.

        CONSTRAINTS:
        1. DOMAIN LIMIT: Only answer questions related to stock market data, technical analysis, and financial metrics.
        2. OUT-OF-SCOPE: If a user asks about the weather, general news, sports, or any non-financial topic, politely decline: "I am a specialized stock copilot. I can only assist with stock analytics and technical data."
        3. DETERMINISTIC ONLY: Never calculate numbers (like SMA, EMA, or price changes) yourself. Always call the appropriate tool.
        4. NO ADVICE: Do not give "buy" or "sell" recommendations. Provide data and interpretations only.
        '''
        
        
    )
)
if response.text:
    print("Final Answer from Agent:", response.text)


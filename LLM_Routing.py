# Using Google Gemini
from pydantic import BaseModel, Field
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from Functions.momentum import get_momentum_status
from Functions.rsi import get_rsi_status
from Functions.macd import get_macd_status
from Functions.volume import get_volume_status
from Functions.volatility import get_volatility_status

df = pd.read_csv('data/raw/daily_bars.csv')

# sample user input
#user_input = 'What is the volatility of Nvidia?'

# ----------------------------------------------
# Define Input Schemas
# ----------------------------------------------
class MomentumInput(BaseModel):
    ticker: str = Field(
        ..., 
        description="The stock ticker symbol in uppercase (e.g., 'AAPL', 'NVDA')."
    )
    window_days: int = Field(
        20, 
        description="The lookback window in days for the moving averages. Common values are 20, 50, or 200."
    )
    
    
class RSIInput(BaseModel):
    ticker: str = Field(
        ..., 
        description="The stock ticker symbol in uppercase (e.g., 'AAPL', 'NVDA')."
    )
    window_days: int = Field(
        14,
        description="Lookback window for RSI calculation. Default is 14 days."
    )


class MACDInput(BaseModel):
    ticker: str = Field(
        ..., 
        description="The stock ticker symbol in uppercase (e.g., 'AAPL', 'NVDA')."
    )


class VolumeInput(BaseModel):
    ticker: str = Field(
        ..., 
        description="The stock ticker symbol in uppercase (e.g., 'AAPL', 'NVDA')."
    )
    window_days: int = Field(
        20,
        description="Lookback window for average volume calculation."
    )


class VolatilityInput(BaseModel):
    ticker: str = Field(
        ..., 
        description="The stock ticker symbol in uppercase (e.g., 'AAPL', 'NVDA')."
    )
    window_days: int = Field(
        30,
        description="Lookback window for volatility calculation."
    )

# ----------------------------------------------
# Tool Wrappers
# ----------------------------------------------

def momentum_tool(ticker: str, window_days: int = 20):
    """
    Analyzes stock momentum by comparing price to SMA and EMA. 
    Use this for questions about price trends, 'bullish' or 'bearish' signs, or if a stock is 'trending'.
    """
    if ticker.upper() not in df['symbol'].unique():
        return {"error": f"Sorry, we do not have the data for the stock you're looking for ({ticker})"}
    return get_momentum_status(df, ticker.upper(), window_days)

def rsi_tool(ticker: str, window_days: int = 14):
    """
    Calculates the Relative Strength Index (RSI). 
    Use this for questions about 'overbought' or 'oversold' conditions, or to check internal price strength.
    """
    if ticker.upper() not in df['symbol'].unique():
        return {"error": f"Sorry, we do not have the data for the stock you're looking for ({ticker})"}
    return get_rsi_status(df, ticker.upper(), window_days)

def macd_tool(ticker: str):
    """
    Calculates Moving Average Convergence Divergence (MACD). 
    Use this to detect momentum shifts and 'crossovers' for entry or exit signals.
    """
    if ticker.upper() not in df['symbol'].unique():
        return {"error": f"Sorry, we do not have the data for the stock you're looking for ({ticker})"}
    return get_macd_status(df, ticker.upper())

def volume_tool(ticker: str, window_days: int = 20):
    """
    Analyzes trading volume compared to its historical average. 
    Use this to check for 'unusual activity', 'liquidity', or 'big money' movement.
    """
    if ticker.upper() not in df['symbol'].unique():
        return {"error": f"Sorry, we do not have the data for the stock you're looking for ({ticker})"}
    return get_volume_status(df, ticker.upper(), window_days)

def volatility_tool(ticker: str, window_days: int = 30):
    """
    Calculates historical volatility. 
    Use this to answer questions about 'risk', 'price swings', 'stability', or how 'choppy' a stock is.
    """
    if ticker.upper() not in df['symbol'].unique():
        return {"error": f"Sorry, we do not have the data for the stock you're looking for ({ticker})"}
    return get_volatility_status(df, ticker.upper(), window_days)

# ----------------------------------------------
# TOOLS Dictionary
# ----------------------------------------------


TOOLS = {
    "get_momentum_status": {
        "function": momentum_tool,
        "schema": MomentumInput,
        "description": "Analyze stock momentum using SMA and EMA"
    },
    "get_rsi_status": {
        "function": rsi_tool,
        "schema": RSIInput,
        "description": "Calculate Relative Strength Index (RSI)"
    },
    "get_macd_status": {
        "function": macd_tool,
        "schema": MACDInput,
        "description": "Analyze MACD indicator and signal line"
    },
    "get_volume_status": {
        "function": volume_tool,
        "schema": VolumeInput,
        "description": "Analyze trading volume compared to historical average"
    },
    "get_volatility_status": {
        "function": volatility_tool,
        "schema": VolatilityInput,
        "description": "Calculate annualized historical volatility"
    }
}

tools_for_llm = []

for tool_name, tool_info in TOOLS.items():
    tools_for_llm.append({
        "type": "function",
        "function": {
            "name": tool_name,
            "description": tool_info["description"],
            "parameters": tool_info["schema"].model_json_schema()
        }
    })
    
tools_config = [
    momentum_tool,
    rsi_tool,
    macd_tool,
    volume_tool,
    volatility_tool
]



# store your api key in the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)
model_id = "gemini-2.5-flash" 



# Model Call
def route_user_question(user_input: str):

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
            2. OUT-OF-SCOPE: If a user asks about the weather, general news, or non-financial topics, decline politely.
            3. DATA AVAILABILITY: If a tool returns an error saying the data is missing for a ticker, inform the user: "Sorry, we do not have the data for the stock you're looking for."
            4. DETERMINISTIC ONLY: Never calculate numbers yourself. Always call the appropriate tool.
            5. NO ADVICE: Provide data and interpretations only; no buy/sell recommendations.
            
            '''
            
        )
    )
    if response.text:
        return f"Final Answer from Agent: {response.text}"    
    else:
        return "No response from LLM."


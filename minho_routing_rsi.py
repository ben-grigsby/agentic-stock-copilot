# Minho 

from pydantic import BaseModel, Field

from rsi_analysis import get_current_rsi

class RsiInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol, e.g. AAPL")
    window_days: int = Field(..., description="Number of days for moving average window")

def rsi_tool(ticker: str, window_days: int):
    return get_current_rsi(ticker, window_days)

TOOLS = {
    "get_current_rsi": {
        "function": rsi_tool,
        "schema": RsiInput,
        "description": "Get the current RSI value and interpretation for a given stock ticker and window size."
    }
}

tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "get_current_rsi",
            "description": TOOLS["get_current_rsi"]["description"],
            "parameters": RsiInput.model_json_schema()
        }
    }
]


from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that provides stock market analysis using RSI data."},
        {"role": "user", "content": user_input}
    ],
    tools=tools_for_llm,
    tool_choice="auto"
)


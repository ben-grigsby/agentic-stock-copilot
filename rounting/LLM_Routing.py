from pydantic import BaseModel, Field

class MomentumInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol, e.g. AAPL")
    window_days: int = Field(..., description="Number of days for moving average window")

def momentum_tool(ticker: str, window_days: int):
    return get_momentum_status(df, ticker, window_days)

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

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You are a stock copilot that uses tools when needed."},
        {"role": "user", "content": user_input}
    ],
    tools=tools_for_llm,
    tool_choice="auto"
)

# Minho

import os 
from pydantic import BaseModel, Field

from relative_performance_analysis import calculate_relative_performance, interpret_relative_performance

class RelativePerformanceInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol, e.g. AAPL")
    benchmark: str = Field(..., description="Benchmark ticker symbol, e.g. SPY")
    window_days: int = Field(..., description="Number of trading days for performance window")

def relative_performance_tool(ticker: str, benchmark: str, window_days: int):
    return calculate_relative_performance(
        dataframe=None,  # This would be replaced with actual data loading logic
        ticker=ticker,
        benchmark=benchmark,
        window_days=window_days
    ), interpret_relative_performance(0.0)  # Placeholder for actual relative return interpretation 

TOOLS = {
    "calculate_relative_performance": {
        "function": relative_performance_tool,
        "schema": RelativePerformanceInput,
        "description": "Calculate the relative performance of a stock against a benchmark over a specified window of trading days."
    }
}

tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "calculate_relative_performance",
            "description": TOOLS["calculate_relative_performance"]["description"],
            "parameters": RelativePerformanceInput.model_json_schema()
        }
    }
]


from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini", # Placeholder for actual model choice
    messages=[
        {"role": "system", "content": "You are a helpful assistant that provides stock market analysis using relative performance data."},
        {"role": "user", "content": user_input}
    ],
    tools=tools_for_llm,
    tool_choice="auto"
)

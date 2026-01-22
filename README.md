# Agentic Stock Copilot

## Overview
This project is a student-led stock analytics system designed to help users explore and understand stocks from a numerical and descriptive perspective. An LLM is used strictly as an intent router to map natural language queries to deterministic analytics functions.

## What This Project Is
- A numerical, exploratory stock analytics engine  
- An example of LLM-orchestrated system design  
- A collaborative project with clearly defined ownership and standards  

## What This Project Is Not
- A trading bot  
- A buy/sell recommendation system  
- A price prediction engine  
- An autonomous or self-reasoning LLM  

## Core Principles 
- The LLM does **not** compute numbers  
- All analytics are deterministic and reproducible  
- All functions must be documented and explain assumptions  
- Failure modes must be explicit (no silent errors)  

## High-Level Architecture
User Query → LLM Intent Routing → Analytics Function → Results + Explanation

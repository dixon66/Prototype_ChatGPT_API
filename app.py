# imports
import openai
import requests
import json
import streamlit as st
import os
 
# Set open AI Keys (read from environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

# Get Crypto API Key from environment variable
crypto_api_key = os.getenv("CRYPTO_API_KEY")

# Load API keys for Crypto API and RapidAPI from config file
with open("config.json") as f:
    config = json.load(f)
    rapid_api_key = config["rapid_api_key"]

# Basic connection with ChatGPT API
def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}]
    )
    return completion.choices[0].message.content

# Get Bitcoin Price From the last 7 days from Crypto API (rapidAPI Example)
def GetBitCoinPrices():
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"7d"}
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    JSONResult = json.loads(response.text)
    history = JSONResult["data"]["history"]
    prices = [change["price"] for change in history]
    pricesList = ','.join(prices)
    return pricesList

def AnalyzeBitCoin(bitcoinPrices):
    chatGPTPrompt = f"""You are an expert crypto trader with more than 10 years of experience, 
    I will provide you with a list of bitcoin prices for the last 7 days
    can you provide me with a technical analysis
    of Bitcoin based on these prices. here is what I want: 
    Price Overview, 
    Moving Averages, 
    Relative Strength Index (RSI),
    Moving Average Convergence Divergence (MACD),
    Advice and Suggestion,
    Do I buy or sell?
    Please be as detailed as you can, and explain in a way any beginner can understand. and make sure to use headings
    Here is the price list: {bitcoinPrices}"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[

                {"role": "user", "content": chatGPTPrompt}
            ]
        )
        message = completion.choices[0].message.content.strip()
    except Exception as e:
        message = "Sorry, I was not able to process your request at this time. Please try again later."
    return message

# Load config and secrets
st.title('ChatGPT Advanced Prompting With Python')
st.subheader(
    'Example: Analyzing Live Crypto Prices')

if st.button('Analyze'):
    with st.spinner('Getting Bitcoin Prices...'):
        bitcoinPrices = GetBitCoinPrices()
        st.success('Done!')
    with st.spinner('Analyzing Bitcoin Prices...'):
        analysis = AnalyzeBitCoin(bitcoinPrices)
        st.text_area("Analysis", analysis,
                     height=500, max_chars=None, key=None,)
        st.success('Done!')

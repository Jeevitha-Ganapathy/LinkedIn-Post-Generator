from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Instantiate the LLM
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama3-8b-8192",  # You can also use mixtral-8x7b-32768 or llama3-70b-8192
    temperature=0.3               # Optional: adjust temperature as needed
)

# Test run (optional)
if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in samosa are")
    print(response.content)

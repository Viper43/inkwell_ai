import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLAMA_MODEL"),
    groq_api_key=os.getenv("GROQ_TOKEN"),
    temperature=0.7
    )

if __name__ == "__main__":
    response = llm.invoke("best cola brand")
    print(response.content)
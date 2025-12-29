from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv

load_dotenv()

def get_model():
    
    model=ChatGroq(model="openai/gpt-oss-120b")
    return model



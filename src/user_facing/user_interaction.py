from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from typing_extensions import TypedDict, Annotated
import operator
from typing import Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel,Field

class ParsedAddress(BaseModel):
    pass

valid_streets = [
    'AVE',
    'CIR',
    'DWY',
    'BLVD',
    'ROW',
    'WALK',
    'DR',
    'ST',
    'PIKE'
]
#working on trying to make an ability to parse target location
#issue currently is that I need to align different ln:lane , ave:aventue etc. 
#also need to make sure everything is capitalized
def query_address(address):
    r"\b\d{1,6}\s+(?:N|S|E|W)?\s*[A-Za-z0-9 .'-]+(?:ST|STREET|AVE|AVENUE|RD|ROAD|BLVD|BOULEVARD|DR|DRIVE|LN|LANE|CT|COURT|PL|PLACE|PKWY|PARKWAY|WAY)\b"


    
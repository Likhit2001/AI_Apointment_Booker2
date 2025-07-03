from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import whisper
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableLambda
import re
import json
import requests

# === STATE ===
class GraphState(TypedDict):
    audio_path: str
    transcription: str
    name: str
    doctor: str
    date: str
    time: str
    reason: str
    contact: str
    email_status: str

# === NODE 1: Whisper Transcriber ===
def whisper_node(state: GraphState) -> GraphState:
    model = whisper.load_model("small")
    result = model.transcribe(state["audio_path"])
    return {**state, "transcription": result["text"]}

# === NODE 2: ChatGroq LLM Extractor ===
api_key = "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"
llm = ChatGroq(model="qwen-qwq-32b", api_key=api_key,temperature=0.0)



def extract_fields(state: GraphState) -> GraphState:
    prompt = f"""
You are an assistant that extracts structured info from transcriptions.
Only return valid JSON with these keys, Only respond with a JSON object. Do not say anything else.:
name, doctor, date, time, reason, contact.

Example output:
{{"name": "John", "doctor": "Dr. Smith", "date": "July 4", "time": "3pm", "reason": "headache", "contact": "7202342341"}}

Now process:
\"\"\"{state['transcription']}\"\"\"
"""

    response = llm.invoke(prompt).content.strip()

    # Extract ONLY the first valid JSON block
    matches = re.findall(r"\{.*?\}", response, re.DOTALL)
    if not matches:
        raise ValueError("No valid JSON object found in LLM response:\n" + response)

    try:
        extracted = json.loads(matches[0])  # only first valid block
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON:\n{matches[0]}\n\nFull response:\n{response}\n\n{str(e)}")

    return {
        **state,
        "name": extracted.get("name", ""),
        "doctor": extracted.get("doctor", ""),
        "date": extracted.get("date", ""),
        "time": extracted.get("time", ""),
        "reason": extracted.get("reason", ""),
        "contact": extracted.get("contact", "")
    }



def send_email_node_and_store_in_s3(state: GraphState) -> GraphState:
    email = state.get("contact", "").lower()
    if not email or "@" not in email:
        return {**state, "email_status": "Skipped: invalid email"}

    params = {
        "name": state.get("name", ""),
        "doctor": state.get("doctor", ""),
        "date": state.get("date", ""),
        "time": state.get("time", ""),
        "email": email
    }

    try:
        response = requests.get("https://n9t1ztj3h7.execute-api.us-east-1.amazonaws.com/V1", params=params)
        if response.ok:
            return {**state, "email_status": "Email has been sent"}
        else:
            print("Status code:", response.status_code)
            print("Text:", response.text)
            print("Headers:", response.headers)
            return {**state, "email_status": f"Failed: {response.text}"}
    except Exception as e:
        return {**state, "email_status": f"Error: {str(e)}"}
    


    

# === BUILD GRAPH ===
workflow = StateGraph(GraphState)

workflow.add_node("whisper_node", whisper_node)
workflow.add_node("extract_node", extract_fields)
workflow.add_node("send_email_node_and_store_in_s3", send_email_node_and_store_in_s3)

workflow.set_entry_point("whisper_node")
workflow.add_edge("whisper_node", "extract_node")
workflow.add_edge("extract_node", "send_email_node_and_store_in_s3")
workflow.add_edge("send_email_node_and_store_in_s3", END)

graph = workflow.compile()

# if __name__ == "__main__":

#     result = graph.invoke({"audio_path": "./sample_audio/likhit.wav"})
#     print("Final State:\n\n\n\n")
#     print(result)
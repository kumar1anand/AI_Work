import gradio as gr
from google import genai
from google.genai import types
client = genai.Client(api_key="AIzaSyCRVlqWju3yBXhV_iJPdI8kSZFPNY08h80")

def chat_fun(message,history):

    contents = []
    for msg in history:
        role = "model" if msg["role"]=="assistant" else "user"
        text = msg["content"]

        if isinstance(text, list):
            text = text[0]["text"]

        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=text)]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)]
        )
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction="Give crisp answers. If unsure, say you are not sure'.",
            temperature=0.7,
            max_output_tokens=200,
        )
    )
    return response.text


gr.ChatInterface(
    fn= chat_fun,
    title="Chat with Gemini",
    description="This is a simple chat interface to interact with Gemini.",
).launch(server_name="0.0.0.0", server_port=7860,share=True)
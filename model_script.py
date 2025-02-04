# model_script.py
# Python script to interact with the deployed DeepSeek AI model on Azure ML
# Supports serverless compute, custom content filtering, and streaming responses

import re
from azure.ai.inference.models import AssistantMessage, UserMessage, SystemMessage
from azure.core.exceptions import HttpResponseError

# Placeholder for Azure client - Ensure to set up authentication securely
client = None  # Replace with actual Azure inference client setup

def get_ai_response(user_input, system_message="You are an AI assistant that helps people find information.", apply_filter=False):
    """
    Fetches AI-generated responses with optional filtering.

    Parameters:
    - user_input (str): The user-provided input text.
    - system_message (str): The system prompt to guide the AI's response.
    - apply_filter (bool): Whether to apply custom filtering logic.

    Returns:
    - str: AI-generated response or an error message.
    """
    try:
        response = client.complete(
            messages=[
                SystemMessage(content=system_message),
                UserMessage(content=user_input),
            ]
        )
        ai_response = response.choices[0].message.content

        # Apply a custom filter if enabled
        if apply_filter:
            ai_response = custom_filter(ai_response)

        return ai_response
    except HttpResponseError as ex:
        if ex.status_code == 400:
            response = ex.response.json()
            if isinstance(response, dict) and "error" in response:
                return f"Your request triggered an {response['error']['code']} error:\n\t {response['error']['message']}"
        raise

def custom_filter(text):
    """
    Custom filtering function to remove specific words from the response.

    Parameters:
    - text (str): The AI-generated response.

    Returns:
    - str: Filtered/moderated text.
    """
    blocked_words = ["knife", "cut", "chop"]  # Modify this list as needed
    for word in blocked_words:
        text = text.replace(word, "[filtered]")
    return text

def print_stream(result):
    """
    Prints the chat completion with streaming.
    """
    for update in result:
        if update.choices:
            print(update.choices[0].delta.content, end="")

if __name__ == "__main__":
    print("🔹 DeepSeek AI Model - Azure ML Serverless Deployment 🔹")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        response = get_ai_response(user_input, apply_filter=True)
        print("AI:", response)

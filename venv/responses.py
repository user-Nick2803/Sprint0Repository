# responses (1).py
import openai
import os
import re
from dotenv import load_dotenv
from conversation import get_conversation_history, update_conversation_history
from data_lookup import lookup_section_tally  # New: import our CSV lookup function

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def is_rowan_related(query: str) -> bool:
    keywords = ['rowan', 'glassboro', 'university']
    return any(keyword in query.lower() for keyword in keywords)

def is_greeting_message(text: str) -> bool:
    pattern = r"\b(hi|hello|hey|greetings|sup|yo|howdy|hiya|good morning|good afternoon|good evening|what's up|what up|how's it going)\b"
    return re.search(pattern, text.lower()) is not None

def get_response(prompt: str, user_id: str = "user") -> str:
    # Retrieve the conversation history for the user.
    history = get_conversation_history(user_id)
    
    # If it's a greeting, reply and skip CSV context.
    if is_greeting_message(prompt.strip()):
        history.append({"role": "user", "content": prompt})
        greeting_response = (
            "Hello! This is the Rowan Chatbot, built to answer important questions regarding Rowan University. "
            "Please keep questions within the context of Rowan, and if you run into any issues please fill out this form: "
            "https://forms.gle/kaMWSJP5fbGqGe7Q7. How can I help you?"
        )
        update_conversation_history(user_id, "assistant", greeting_response)
        return greeting_response
    
    # On the very first interaction, enforce that the query is Rowan-related.
    if len(history) == 1 and not is_rowan_related(prompt):
        return "I'm sorry, I can only answer questions about Rowan University. Please ask something related to Rowan University."
    
    # Identify if the query likely pertains to class/section data (searching for a wide range of keywords).
    csv_keywords = ["section", "course", "class", "campus", "tally", "department", "time", "professor", "instructor"]
    if any(word in prompt.lower() for word in csv_keywords):
        # Retrieve relevant CSV data based on the user's query.
        csv_context = lookup_section_tally(prompt)
        # Prepend the CSV context to the query.
        prompt_with_context = (
            f"Based on the following CSV data from the Section Tally file:\n\n{csv_context}\n\n"
            f"Answer the following question about university classes at Rowan University:\n{prompt}"
        )
    else:
        prompt_with_context = prompt

    # Append the (possibly augmented) user message to the conversation history.
    history.append({"role": "user", "content": prompt_with_context})
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
            user=user_id
        )
        response = completion.choices[0].message.content.strip()
        update_conversation_history(user_id, "assistant", response)
        return response
    except Exception as e:
        return f"Error from OpenAI: {e}"

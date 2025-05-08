import openai
import os
import re
import pandas as pd
from dotenv import load_dotenv
from conversation import get_conversation_history, update_conversation_history
from data_lookup import get_section_dataframe

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the trimmed Section Tally DataFrame
df = get_section_dataframe()

# Track pending section lookups for each user
pending_sections: dict[str, pd.DataFrame] = {}

# Greeting detection pattern
greeting_pattern = r"\b(hi|hello|hey|greetings|sup|yo|howdy|hiya|good morning|good afternoon|good evening|what's up|what up|how's it going)\b"

def is_greeting_message(text: str) -> bool:
    return re.search(greeting_pattern, text.lower()) is not None

# Rowan University context enforcement
def is_rowan_related(query: str) -> bool:
    keywords = ['rowan', 'glassboro', 'university']
    return any(k in query.lower() for k in keywords)

def get_response(prompt: str, user_id: str = "user") -> str:
    # Debug: log incoming prompt
    print(f"DEBUG: get_response prompt='{prompt}' user_id={user_id}")
    
    # Debug: Check DataFrame state
    print("DEBUG: Initial DataFrame State:")
    print(f"DEBUG: DataFrame shape: {df.shape}")
    print(f"DEBUG: Available columns: {list(df.columns)}")
    print(f"DEBUG: First few rows:")
    print(df.head())
    print("\n")

    history = get_conversation_history(user_id)

    # 1) Greeting short-circuit
#    if is_greeting_message(prompt):
#        print("DEBUG: matched greeting handler")
#        history.append({"role": "user", "content": prompt})
#        greeting = (
#            "Hello! This is the Rowan Chatbot, built to answer important questions regarding Rowan University. "
#            "Please keep questions within the context of Rowan, and if you run into any issues please fill out "
#            "this form: https://forms.gle/kaMWSJP5fbGqGe7Q7. How can I help you?"
#        )
#        update_conversation_history(user_id, "assistant", greeting)
#        return greeting

    # 2) Interactive !section command
    if prompt.lower().startswith("!section"):
        print("DEBUG: matched !section handler")
        
        # Debug: Show current pending sections
        print("DEBUG: Current pending_sections dictionary:")
        print(pending_sections)
        print("\n")
        
        parts = prompt.split(maxsplit=1)
        filter_text = parts[1] if len(parts) > 1 else ""
        
        try:
            df_filtered = df.copy()
            print(f"DEBUG: Searching for '{filter_text}' in DataFrame")
            
            # Improved filtering logic
            mask = df['Subj'].str.contains(filter_text, case=False, na=False)
            df_filtered = df[mask]
            
            print(f"DEBUG: Found {len(df_filtered)} matching courses")
            
            if df_filtered.empty:
                return f"No sections found matching '{filter_text}'. Try a different keyword."
            
            # Show first few matches for debugging
            print("\nDEBUG: First few matching courses:")
            print(df_filtered[['CRN', 'Subj', 'Crse', 'Sect']].head())
            
            df_list = df_filtered.head(10).reset_index(drop=True)
            pending_sections[user_id] = df_list
            
            print("\nDEBUG: Updated pending_sections dictionary:")
            print(pending_sections)
            
            lines = ["Here are the matching sections—reply with the number for full details:"]
            for i, row in df_list.iterrows():
                lines.append(f"{i+1}. CRN {row['CRN']}, {row['Subj']}{row['Crse']} sec {row['Sect']}")
            return "\n".join(lines)
            
        except Exception as e:
            print(f"DEBUG ERROR: Error processing section request: {str(e)}")
            return f"Error processing section request: {str(e)}"
    
    # 3) Numeric reply for a pending !section list
    if prompt.isdigit() and user_id in pending_sections:
        print("DEBUG: matched numeric selection handler")
        
        choice = int(prompt) - 1
        df_list = pending_sections.pop(user_id)
        
        print(f"DEBUG: Selected index: {choice}")
        print(f"DEBUG: Available options count: {len(df_list)}")
        
        if choice < 0 or choice >= len(df_list):
            print("DEBUG: Invalid selection made")
            return "That number isn't in the list. Please choose a valid number."
            
        row = df_list.iloc[choice]
        detail_lines = [f"**{col}**: {row[col]}" for col in df_list.columns]
        return "\n".join(detail_lines)

    # 4) Enforce Rowan-only on first non-!section message
    if len(history) == 1 and not is_rowan_related(prompt):
        print("DEBUG: matched first-message Rowan enforcement")
        return "Sorry, I can only answer questions about Rowan University. Please ask something about Rowan."

    # 5) Fallback to OpenAI API
    print("DEBUG: falling back to OpenAI completion")
    
    history.append({"role": "user", "content": prompt})
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
            user=user_id
        )
        
        print("DEBUG: OpenAI completion successful")
        print(f"DEBUG: Response length: {len(completion.choices[0].message.content)}")
        
        response = completion.choices[0].message.content.strip()
        update_conversation_history(user_id, "assistant", response)
        return response
        
    except Exception as e:
        print(f"DEBUG ERROR: OpenAI API error: {str(e)}")
        return f"An error occurred while processing your request: {str(e)}. Please try again."
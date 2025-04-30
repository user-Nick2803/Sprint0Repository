# conversation.py
# This module manages conversation history for stateful interactions per user.

# A dictionary to store conversation history for each user by their ID.
conversation_history = {}

def get_conversation_history(user_id: str):
    """
    Retrieve or initialize the conversation history for a given user.
    """
    if user_id not in conversation_history:
        # Initialize with a system message that sets context.
        conversation_history[user_id] = [
            {
                "role": "system",
                "content": "You are an expert on Rowan University. Answer the following question with information relevant only to Rowan University."
            }
        ]
    return conversation_history[user_id]

def update_conversation_history(user_id: str, role: str, content: str):
    """
    Append a new message to the conversation history for a given user.
    """
    history = get_conversation_history(user_id)
    history.append({"role": role, "content": content})

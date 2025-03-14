import random
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./fine_tuned_gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('./fine_tuned_gpt2')

tokenizer.pad_token = tokenizer.eos_token


# Define pre-defined responses and intent keywords
responses = {
    "greeting": [
        "Hello! How can I assist you today?",
        "Hi there! How can I help you?",
        "Greetings! How can I support you?"
    ],
    "about_calisnova": [
        "Calisnova is an innovative platform focused on empowering students with essential life skills.",
        "At Calisnova, we believe in fostering personal growth through practical, real-world learning experiences."
    ],
    "courses": [
        "We offer a variety of courses to help students develop skills in leadership, innovation, and critical thinking.",
        "Our courses are designed to equip students with the skills they need to succeed in the modern world."
    ],
    # Additional predefined intents can be added here...
    "unknown": [
        "Sorry, I didn't quite understand that. Could you please rephrase?",
        "I’m not sure how to help with that. Can you clarify?"
    ]
}

intent_keywords = {
    "greeting": ["hello", "hi", "hey", "greetings", "howdy", "morning", "evening"],
    "about_calisnova": ["calisnova", "about", "what is", "who are we", "tell me about", "mission"],
    "courses": ["courses", "classes", "offer", "teach", "programs", "subjects"]
    # Additional keywords can be added here...
}

# Define request schema
class ChatRequest(BaseModel):
    user_input: str

# Intent detection function
def get_intent(user_input):
    user_input = user_input.lower()
    for intent, keywords in intent_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return intent
    return "unknown"

# Function to generate response using the fine-tuned GPT model
def generate_finetuned_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model.generate(
        inputs["input_ids"],
        max_length=150,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=inputs["attention_mask"],
        no_repeat_ngram_size=2
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to get response based on intent
def chatbot_response(user_input):
    intent = get_intent(user_input)
    if intent != "unknown":
        return random.choice(responses[intent])
    return generate_finetuned_response(user_input)

# FastAPI endpoint for chatbot interaction
@app.post("/chat/")
def chat(request: ChatRequest):
    response = chatbot_response(request.user_input)
    return {"response": response}

# Console-based chat loop
def console_chat():
    print("Chatbot: Hello! I am Calisnova's assistant. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")

# Run the console chat only if executed directly
if __name__ == "__main__":
    console_chat()

   


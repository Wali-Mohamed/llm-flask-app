# rag.py

import time
from openai import OpenAI
import minsearch
import local_ingest
import json
import os


# Initialize the OpenAI client
client = OpenAI()


index = local_ingest.load_index()

def search(query):
    boost = {
        'content': 1.9366969407339725
    }
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )
    return results

def build_prompt(query, search_results):
    prompt_template = """
    You're a primal health adviser. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT: 
    {context}
    """.strip()

    context = "\n".join([f"content: {doc['content']}" for doc in search_results])
    
    return prompt_template.format(question=query, context=context).strip()

def llm(prompt):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def rag(query):
    # Check if the user is asking who created the bot
    if query.lower() in ["who created you?", "who is your creator?", "who made you?"]:
        return "I was created by W Mohamed."

    # Otherwise, proceed with normal search and LLM response
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    time.sleep(1)  # Simulating a delay for the function to work
    return answer
    

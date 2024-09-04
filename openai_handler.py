import os
from openai import OpenAI
import json

client = OpenAI()

def load_system_prompt(file_path="systemprompt.txt"):
    """
    Load the system prompt from a local file to instruct the LLM how to behave.

    :param file_path: The path to the system prompt file
    :return: The contents of the system prompt
    """
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        return f"Error loading system prompt: {str(e)}"


# Function to send prompt to OpenAI and receive response in JSON format
def generate_response(prompt, model="gpt-4o"):
    """
    Send a prompt to OpenAI's GPT model and receive a response as a JSON object.

    :param prompt: The input prompt (user's question or conversation context)
    :param model: The GPT model to use (default: gpt-3.5-turbo)
    :return: JSON response containing the type (query/modify) and the Cypher query
    """
    try:
        # Load the system prompt from the file
        system_prompt = load_system_prompt()

        # Send the system prompt and user input to OpenAI
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Let's parse the content to check if it's valid JSON
        generated_content = response.choices[0].message.content.strip()

        return generated_content

    except Exception as e:
        return {"status": "Error", "message": str(e)}


# Function to convert Cypher query result to conversational text
def interpret_cypher_result(cypher_query, cypher_result):
    """
    Takes a Cypher query and its result, and sends it to the LLM to generate
    a more human-readable, conversational response.

    :param cypher_query: The original Cypher query sent to Neo4j
    :param cypher_result: The result from the Cypher query execution
    :return: Human-readable, conversational interpretation of the result
    """
    system_prompt = "You're a helpful assistant that turns raw Cypher query results into conversational language."
    prompt = f"Take the following Cypher query and result, and turn it into a conversational, human-readable response:\n\nQuery: {cypher_query}\n\nResult: {cypher_result}"

    try:

        # Send the prompt to OpenAI to interpret the result
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Return the interpretation
        generated_content = response.choices[0].message.content.strip()
        return generated_content

    except Exception as e:
        return f"Error interpreting results: {str(e)}"
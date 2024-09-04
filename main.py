from openai_handler import generate_response, interpret_cypher_result
from neo4j_handler import execute_cypher_modify, execute_cypher_query
import json
import re


def handle_conversation():
    """
    Handles user interaction, assumes it's a normal conversation unless the LLM response
    contains a Cypher query (indicated by the presence of 'type' and 'cypher_query' fields).
    If both plain text and JSON are returned, handle them appropriately.
    """
    while True:
        # Get user input
        user_input = input("User: ")

        # Break loop if user types 'exit'
        if user_input.lower() == 'exit':
            print("Exiting conversation.")
            break

        # Generate response from OpenAI
        ai_response = generate_response(user_input)

        # Detect if the response contains JSON (within curly braces)
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)

        if json_match:
            # Extract the JSON part
            json_part = json_match.group(0).strip()

            # Extract the plain text part (if any)
            plain_text_part = ai_response.replace(json_part, '').strip()
            if plain_text_part:
                print(f"Assistant: {plain_text_part}")

            # Attempt to parse the JSON part
            try:
                parsed_response = json.loads(json_part)

                # Check for required keys in the JSON
                if "type" in parsed_response and "cypher_query" in parsed_response:
                    operation_type = parsed_response["type"]
                    cypher_query = parsed_response["cypher_query"]

                    print(f"Generated Cypher Query: {cypher_query}")

                    # Ask the user if they'd like to execute the query
                    execute_query = input("Do you want to execute this Cypher query? (yes/no): ").lower()
                    if execute_query == "yes":
                        # Choose the appropriate function based on the operation type
                        if operation_type == "query":
                            cypher_result = execute_cypher_query(cypher_query)
                            result = interpret_cypher_result(cypher_query, cypher_result)
                            print(result)
                        elif operation_type == "modify":
                            result = execute_cypher_modify(cypher_query)
                            print(f"Modify Result: {result}")
                        else:
                            print("Unknown operation type. Skipping execution.")
                    else:
                        print("Skipping execution.")
                else:
                    print("Invalid JSON format. Skipping execution.")
            except json.JSONDecodeError:
                print("Failed to parse the JSON part of the response. Please try again.")
        else:
            # If there's no JSON, treat it as plain text
            print(f"Assistant: {ai_response}")

    # Close the Neo4j connection when done
    from neo4j_handler import close_driver
    close_driver()


if __name__ == "__main__":
    handle_conversation()

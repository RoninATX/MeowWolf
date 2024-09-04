import os
from neo4j import GraphDatabase

# fetch Neo4j connection details from environment variables
uri = os.getenv("GRAPH_URL")
username = os.getenv("GRAPH_UNAME")
password = os.getenv("GRAPH_PASSWORD")

# Initialize the driver
driver = GraphDatabase.driver(uri, auth=(username, password))


# Function to execute Cypher queries for modifications (CREATE, MERGE, DELETE, etc.)
def execute_cypher_modify(query, params=None):
    """
    Execute a Cypher query that modifies the graph (CREATE, MERGE, DELETE, etc.)

    :param query: The Cypher query string
    :param params: Parameters to pass into the query (optional)
    :return: Confirmation message or error details
    """
    with driver.session() as session:
        try:
            session.run(query, params)
            return {"status": "Success", "message": "Query executed successfully"}
        except Exception as e:
            return {"status": "Error", "message": str(e)}


# Function to execute Cypher queries for retrieving data (MATCH, RETURN, etc.)
def execute_cypher_query(query, params=None):
    """
    Execute a Cypher query to retrieve data from the graph (MATCH, RETURN, etc.)

    :param query: The Cypher query string
    :param params: Parameters to pass into the query (optional)
    :return: The result of the query (list of records)
    """
    with driver.session() as session:
        try:
            result = session.run(query, params)
            return [record.data() for record in result]
        except Exception as e:
            return {"status": "Error", "message": str(e)}


# Close the driver when done
def close_driver():
    driver.close()

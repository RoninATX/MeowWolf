# MeowWolf
Graph Data for the Meow Wolf universe.

# Conversational Lore and Updates
Over the next few releases I'll be implementing GPT as a go-between with the database. It leverages a special system prompt found in `systemprompt.txt`

# GPT Interface Prerequisites
To implement the same for your instance you will need:
1. An Open AI API Key with permissions to talk to whatever model you want to use.
2. The Neo4j URI for wherever your database is hosted:

![image](https://github.com/user-attachments/assets/734f8d80-54ea-49d8-9f05-4fd07149173d)

3: The username and password for your Neo4j database.

Set these as the following environment variables in your project:

![image](https://github.com/user-attachments/assets/a46b041b-8b1d-4b80-ae7f-c9a7ef552de7)

# Interaction Examples:
Conversationally asking GPT to return the current list of Meow Wolf Locations:

![image](https://github.com/user-attachments/assets/960f7ea7-2514-4534-8c18-607bba2c4ea9)

Conversationally asking GPT to add a new Location:

![image](https://github.com/user-attachments/assets/27c6c920-c291-48ab-ae75-36d3d1999a7c)

# Current Limitations
1. This release is currently very basic and lacks long term conversation tracking as it was a proof of concept for querying and writing back to the Graph DB.
2. Since there is no conversation history so you can't really do follow up exploration type questioning (yet)
3. It doesn't begin with an automatic semantic understanding of the graph DB. The examples in the screenshot "worked" because I happen to use an obvious node type "Location".  

# Next Release:
1. Conversation history
2. And "audo discovery" boot up sequence that will study the Graph DB to produce a cached list of node types, relationship types, and property attributes so that it can more effectively arrive at the correct syntax.

# from flask import Flask, request, render_template
# from aiml import Kernel
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer
# from nltk.tokenize import word_tokenize
# from nltk import pos_tag
# from nltk.corpus import wordnet as wn
# import spacy
# import pytholog as pl
# from neo4j import GraphDatabase
#
# # Download required NLTK resources (only the first time)
# # nltk.download('wordnet')
# # nltk.download('omw-1.4')
# # nltk.download('vader_lexicon')  # For sentiment analysis
# # nltk.download('punkt')  # For tokenization
# # nltk.download('averaged_perceptron_tagger')  # For POS tagging
#
# # Load spaCy English model
# nlp = spacy.load("en_core_web_sm")
#
# # Initialize AIML Kernel
# bot = Kernel()
#
# # Load AIML files
# bot.learn(r"D:\JN\Fitness_chatbot\*.aiml")
#
# # Initialize Prolog knowledge base
# kb = pl.KnowledgeBase("fitness_kb")
# kb.clear_cache()
# kb.from_file(r"D:\JN\Fitness_chatbot\fitness_kb.pl")  # Ensure the correct path to the Prolog file
#
# # Set bot predicates
# bot.setBotPredicate("master", "ABDULLAH")
# bot.setBotPredicate("order", "ASSISTANT")
# bot.setBotPredicate("name", "JARVIS")
# bot.setPredicate("name", "Mr.ABDULLAH")
#
# # Initialize Sentiment Analyzer
# sentiment_analyzer = SentimentIntensityAnalyzer()
#
# # Neo4j connection setup (adjust credentials as needed)
# driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "23704300"))
#
#
# # Function to create a person node in Neo4j
# def create_person_node(person_name):
#     try:
#         with driver.session() as session:
#             cypher_query = (
#                 "MERGE (p:Person {name: $person_name}) "
#                 "RETURN p"
#             )
#             result = session.run(cypher_query, person_name=person_name)
#             print(f"Created node: {person_name}")
#             return result
#     except Exception as e:
#         print(f"Error creating node in Neo4j: {e}")
#         return None
#
#
# # Function to create a relationship between two people
# def create_relationship(person1, person2, relationship_type):
#     try:
#         with driver.session() as session:
#             cypher_query = (
#                 "MERGE (p1:Person {name: $person1}) "
#                 "MERGE (p2:Person {name: $person2}) "
#                 f"MERGE (p1)-[:{relationship_type.upper()}]->(p2) "
#                 "RETURN p1, p2"
#             )
#             result = session.run(cypher_query, person1=person1, person2=person2)
#             print(f"Created relationship: {person1} -[{relationship_type}]-> {person2}")
#             return result
#     except Exception as e:
#         print(f"Error creating relationship in Neo4j: {e}")
#         return None
#
#
# # Function to delete a relationship and nodes if they have no other relationships
# def delete_relationship_and_nodes(person1, person2, relationship_type):
#     try:
#         with driver.session() as session:
#             # Delete the relationship
#             delete_relationship_query = (
#                 "MATCH (p1:Person {name: $person1})-[r]->(p2:Person {name: $person2}) "
#                 "WHERE type(r) = $relationship_type "
#                 "DELETE r "
#                 "RETURN p1, p2"
#             )
#             session.run(
#                 delete_relationship_query,
#                 person1=person1,
#                 person2=person2,
#                 relationship_type=relationship_type.upper()
#             )
#             print(f"Deleted relationship: {person1} -[{relationship_type}]-> {person2}")
#
#             # Delete nodes if they have no other relationships
#             delete_orphaned_nodes_query = (
#                 "MATCH (p:Person) "
#                 "WHERE NOT (p)--() "
#                 "DELETE p "
#                 "RETURN p"
#             )
#             result = session.run(delete_orphaned_nodes_query)
#             for record in result:
#                 print(f"Deleted orphaned node: {record['p']['name']}")
#     except Exception as e:
#         print(f"Error deleting relationship or nodes in Neo4j: {e}")
#
#
# # Function to find the relationship between two people
# def find_relationship(person1, person2):
#     try:
#         with driver.session() as session:
#             cypher_query = (
#                 "MATCH (p1:Person {name: $person1})-[r]->(p2:Person {name: $person2}) "
#                 "RETURN type(r) AS relationship_type"
#             )
#             result = session.run(cypher_query, person1=person1, person2=person2)
#             relationships = [record["relationship_type"] for record in result]
#             return relationships
#     except Exception as e:
#         print(f"Error finding relationship in Neo4j: {e}")
#         return None
#
#
# # Function to handle Neo4j-related queries
# def handle_neo4j_query(query):
#     if " is a " in query and " of " in query:
#         try:
#             # Extract names and relationship type from the input
#             parts = query.split(" is a ")
#             person1 = parts[0].strip()
#             relationship_part = parts[1].split(" of ")
#             relationship_type = relationship_part[0].strip()
#             person2 = relationship_part[1].strip()
#
#             # Create nodes and relationship in Neo4j
#             create_person_node(person1)
#             create_person_node(person2)
#             create_relationship(person1, person2, relationship_type)
#
#             return f"I have recorded that {person1} is a {relationship_type} of {person2}."
#         except Exception as e:
#             return f"Error while processing your input: {e}"
#
#     elif " is not a " in query and " of " in query:
#         try:
#             # Extract names and relationship type from the input
#             parts = query.split(" is not a ")
#             person1 = parts[0].strip()
#             relationship_part = parts[1].split(" of ")
#             relationship_type = relationship_part[0].strip()
#             person2 = relationship_part[1].strip()
#
#             # Delete the relationship and orphaned nodes in Neo4j
#             delete_relationship_and_nodes(person1, person2, relationship_type)
#
#             return f"I have deleted the relationship that {person1} is a {relationship_type} of {person2}."
#         except Exception as e:
#             return f"Error while processing your input: {e}"
#
#     elif "find the relationship between" in query:
#         try:
#             # Extract names from the input
#             parts = query.split("find the relationship between")
#             names = parts[1].strip().split(" and ")
#             person1 = names[0].strip()
#             person2 = names[1].strip()
#
#             # Find the relationship in Neo4j
#             relationships = find_relationship(person1, person2)
#
#             if relationships:
#                 return f"The relationship between {person1} and {person2} is: {', '.join(relationships)}"
#             else:
#                 return f"No relationship found between {person1} and {person2}."
#         except Exception as e:
#             return f"Error while processing your input: {e}"
#
#     return None
#
#
# # Function to query Prolog knowledge base
# def query_prolog(relation, entity):
#     """Query the Prolog knowledge base for a relation and entity."""
#     expr = f"{relation}(Y, {entity})"  # Construct Prolog query
#     results = kb.query(pl.Expr(expr))
#     if results:
#         # Extract all values of 'Y' from the results and remove duplicates
#         all_results = list(set([result.get('Y') for result in results]))
#         return all_results
#     else:
#         print(f"No results found for query: {expr}")
#         return None
#
#
# # Function to handle relation-based queries using AIML and Prolog
# def handle_relation_query(user_input):
#     """Handle relation-based queries using AIML and Prolog."""
#     # Respond to the user input to set AIML predicates
#     bot_response = bot.respond(user_input)
#
#     # Retrieve the relation and entity from AIML predicates
#     relation = bot.getPredicate("rel")
#     entity = bot.getPredicate("X")
#
#     if not relation or not entity:
#         print("Error: Missing relation or entity in AIML predicates.")
#         return bot_response
#
#     # Query Prolog using the retrieved relation and entity
#     result = query_prolog(relation, entity)
#
#     if result:
#         # Convert the list of results to a comma-separated string
#         result_str = ", ".join(result)
#         # Store the result back in AIML
#         bot.setPredicate("Y", result_str)  # "Y" will store the Prolog query result as a string
#         bot_response += f"\n[Prolog Result: {result_str}]"
#     else:
#         print(f"No relation found for {relation} of {entity}.")
#         bot.setPredicate("Y", "unknown")  # Set "unknown" if no result is found
#         bot_response += "\n[Prolog Result: No information found.]"
#
#     # Clear the relation and entity predicates after the query
#     bot.setPredicate("rel", "")
#     bot.setPredicate("X", "")
#
#     return bot_response
#
#
# # Function to handle WordNet-based definition queries
# # Function to handle WordNet-based definition queries
# def handle_definition_query(query):
#     try:
#         # Extract the word to define
#         word = query.lower().replace("what is ", "").replace("define ", "").strip("?.")
#
#         # Fetch synsets for the word
#         synsets = wn.synsets(word)
#
#         # If no synsets are found, return a user-friendly message
#         if not synsets:
#             return f"Sorry, I couldn't find a definition for '{word}' in my database."
#
#         # Format multiple senses if available
#         definitions = [f"{i + 1}. {synset.definition()}" for i, synset in enumerate(synsets)]
#         return f"Here are the definitions for '{word}':\n" + "\n".join(definitions)
#     except Exception as e:
#         # Log the error for debugging
#         print(f"Error fetching definition for '{word}': {e}")
#         return f"An error occurred while fetching the definition for '{word}'. Please try again."
#
#
# # Function to perform sentiment analysis
# def perform_sentiment_analysis(sentence):
#     try:
#         # Analyze sentiment using VADER
#         sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
#         compound_score = sentiment_scores['compound']
#
#         # Determine sentiment based on compound score
#
#         if compound_score == 0:
#             sentiment = "Neutral 😐"
#         elif compound_score > 0:
#             sentiment = "Positive 😊"
#         elif compound_score < 0:
#             sentiment = "Negative 😠"
#
#
#         return sentiment, compound_score
#     except Exception as e:
#         # Log the error for debugging
#         print(f"Error performing sentiment analysis: {e}")
#         return "Unknown", 0.0
#
#
# # Initialize Flask app
# app = Flask(__name__)
#
# # Login credentials
# VALID_USERNAME = "abdullah"
# VALID_PASSWORD = "abd123"
#
#
# # Route for login page
# @app.route('/')
# def login_page():
#     return render_template('login.html')
#
#
# # Route to handle login form submission
# @app.route('/login', methods=['POST'])
# def login():
#     username = str(request.form.get('username'))
#     password = str(request.form.get('password'))
#     if username == VALID_USERNAME and password == VALID_PASSWORD:
#         return render_template('home.html')
#     else:
#         return """
#         <script>
#             alert('Invalid credentials, please try again.');
#             window.location.href = '/';
#         </script> """
#
# @app.route("/get")
# def get_bot_response():
#     # Retrieve user query
#     query = request.args.get('msg')
#     print(f"User Query: {query}")  # Debugging: Print the user query
#
#     # Handle definition queries first
#     if query.lower().startswith(("what is ", "define ")):
#         definition_response = handle_definition_query(query)
#         return definition_response
#
#     # Handle Neo4j-related queries
#     neo4j_response = handle_neo4j_query(query)
#     if neo4j_response:
#         return neo4j_response
#
#     # Handle Prolog-related queries
#     # prolog_response = handle_relation_query(query)
#     # if prolog_response:
#     #     return prolog_response
#
#     # Perform sentiment analysis
#     sentiment, compound_score = perform_sentiment_analysis(query)
#     bot.setPredicate("last_sentiment", sentiment)  # Save sentiment as predicate
#
#     # Debugging: Print sentiment analysis result
#     print(f"Sentiment: {sentiment}, Compound Score: {compound_score}")
#
#     # Default AIML response
#     bot_response = bot.respond(query)
#     if not bot_response:
#         bot_response = "I'm sorry, I don't understand that yet."
#
#     # Conditionally append sentiment analysis result if relevant
#     if "feel" in query.lower() or "mood" in query.lower():
#         bot_response += f" Based on your input, your mood seems to be {sentiment}."
#
#     # Debugging: Print final bot response
#     print(f"Final Bot Response: {bot_response}")
#
#     return bot_response
# if __name__ == "__main__":
#     # Run Flask app
#     app.run(host="0.0.0.0", port=5000, debug=True)









from flask import Flask, request, render_template
from aiml import Kernel
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
import spacy
import pytholog as pl
from neo4j import GraphDatabase

# Download required NLTK resources (only the first time)
nltk.download('wordnet')
nltk.download('omw-1.4')
# nltk.download('vader_lexicon')  # For sentiment analysis
# nltk.download('punkt')  # For tokenization
# nltk.download('averaged_perceptron_tagger')  # For POS tagging

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize AIML Kernel
bot = Kernel()

# Load AIML files
bot.learn(r"D:\JN\Fitness_chatbot\*.aiml")

# Initialize Prolog knowledge base
kb = pl.KnowledgeBase("fitness_kb")
kb.clear_cache()
kb.from_file(r"D:\JN\Fitness_chatbot\fitness_kb.pl")  # Ensure the correct path to the Prolog file

# Set bot predicates
bot.setBotPredicate("master", "ABDULLAH")
bot.setBotPredicate("order", "ASSISTANT")
bot.setBotPredicate("name", "JARVIS")
bot.setPredicate("name", "Mr.ABDULLAH")

# Initialize Sentiment Analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Neo4j connection setup (adjust credentials as needed)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "23704300"))

# Function to create a person node in Neo4j
def create_person_node(person_name):
    try:
        with driver.session() as session:
            cypher_query = (
                "MERGE (p:Person {name: $person_name}) "
                "RETURN p"
            )
            result = session.run(cypher_query, person_name=person_name)
            print(f"Created node: {person_name}")
            return result
    except Exception as e:
        print(f"Error creating node in Neo4j: {e}")
        return None

# Function to create a relationship between two people
def create_relationship(person1, person2, relationship_type):
    try:
        with driver.session() as session:
            cypher_query = (
                "MERGE (p1:Person {name: $person1}) "
                "MERGE (p2:Person {name: $person2}) "
                f"MERGE (p1)-[:{relationship_type.upper()}]->(p2) "
                "RETURN p1, p2"
            )
            result = session.run(cypher_query, person1=person1, person2=person2)
            print(f"Created relationship: {person1} -[{relationship_type}]-> {person2}")
            return result
    except Exception as e:
        print(f"Error creating relationship in Neo4j: {e}")
        return None

# Function to delete a relationship and nodes if they have no other relationships
def delete_relationship_and_nodes(person1, person2, relationship_type):
    try:
        with driver.session() as session:
            # Delete the relationship
            delete_relationship_query = (
                "MATCH (p1:Person {name: $person1})-[r]->(p2:Person {name: $person2}) "
                "WHERE type(r) = $relationship_type "
                "DELETE r "
                "RETURN p1, p2"
            )
            session.run(
                delete_relationship_query,
                person1=person1,
                person2=person2,
                relationship_type=relationship_type.upper()
            )
            print(f"Deleted relationship: {person1} -[{relationship_type}]-> {person2}")

            # Delete nodes if they have no other relationships
            delete_orphaned_nodes_query = (
                "MATCH (p:Person) "
                "WHERE NOT (p)--() "
                "DELETE p "
                "RETURN p"
            )
            result = session.run(delete_orphaned_nodes_query)
            for record in result:
                print(f"Deleted orphaned node: {record['p']['name']}")
    except Exception as e:
        print(f"Error deleting relationship or nodes in Neo4j: {e}")

# Function to find the relationship between two people
def find_relationship(person1, person2):
    try:
        with driver.session() as session:
            cypher_query = (
                "MATCH (p1:Person {name: $person1})-[r]->(p2:Person {name: $person2}) "
                "RETURN type(r) AS relationship_type"
            )
            result = session.run(cypher_query, person1=person1, person2=person2)
            relationships = [record["relationship_type"] for record in result]
            return relationships
    except Exception as e:
        print(f"Error finding relationship in Neo4j: {e}")
        return None

# Function to handle Neo4j-related queries
def handle_neo4j_query(query):
    if " is a " in query and " of " in query:
        try:
            # Extract names and relationship type from the input
            parts = query.split(" is a ")
            person1 = parts[0].strip()
            relationship_part = parts[1].split(" of ")
            relationship_type = relationship_part[0].strip()
            person2 = relationship_part[1].strip()

            # Create nodes and relationship in Neo4j
            create_person_node(person1)
            create_person_node(person2)
            create_relationship(person1, person2, relationship_type)

            return f"I have recorded that {person1} is a {relationship_type} of {person2}."
        except Exception as e:
            return f"Error while processing your input: {e}"

    elif " is not a " in query and " of " in query:
        try:
            # Extract names and relationship type from the input
            parts = query.split(" is not a ")
            person1 = parts[0].strip()
            relationship_part = parts[1].split(" of ")
            relationship_type = relationship_part[0].strip()
            person2 = relationship_part[1].strip()

            # Delete the relationship and orphaned nodes in Neo4j
            delete_relationship_and_nodes(person1, person2, relationship_type)

            return f"I have deleted the relationship that {person1} is a {relationship_type} of {person2}."
        except Exception as e:
            return f"Error while processing your input: {e}"

    elif "find the relationship between" in query:
        try:
            # Extract names from the input
            parts = query.split("find the relationship between")
            names = parts[1].strip().split(" and ")
            person1 = names[0].strip()
            person2 = names[1].strip()

            # Find the relationship in Neo4j
            relationships = find_relationship(person1, person2)

            if relationships:
                return f"The relationship between {person1} and {person2} is: {', '.join(relationships)}"
            else:
                return f"No relationship found between {person1} and {person2}."
        except Exception as e:
            return f"Error while processing your input: {e}"

    return None

# Function to query Prolog knowledge base
def query_prolog(relation, entity):
    """Query the Prolog knowledge base for a relation and entity."""
    expr = f"{relation}(Y, {entity})"  # Construct Prolog query
    results = kb.query(pl.Expr(expr))
    if results:
        # Extract all values of 'Y' from the results and remove duplicates
        all_results = list(set([result.get('Y') for result in results]))
        return all_results
    else:
        print(f"No results found for query: {expr}")
        return None

# Function to handle relation-based queries using AIML and Prolog
def handle_relation_query(user_input):
    """Handle relation-based queries using AIML and Prolog."""
    # Respond to the user input to set AIML predicates
    bot_response = bot.respond(user_input)

    # Retrieve the relation and entity from AIML predicates
    relation = bot.getPredicate("rel")
    entity = bot.getPredicate("X")

    if not relation or not entity:
        print("Error: Missing relation or entity in AIML predicates.")
        return bot_response

    # Query Prolog using the retrieved relation and entity
    result = query_prolog(relation, entity)

    if result:
        # Convert the list of results to a comma-separated string
        result_str = ", ".join(result)
        # Store the result back in AIML
        bot.setPredicate("Y", result_str)  # "Y" will store the Prolog query result as a string
        bot_response += f"\n[Prolog Result: {result_str}]"
    else:
        print(f"No relation found for {relation} of {entity}.")
        bot.setPredicate("Y", "unknown")  # Set "unknown" if no result is found
        bot_response += "\n[Prolog Result: No information found.]"

    # Clear the relation and entity predicates after the query
    bot.setPredicate("rel", "")
    bot.setPredicate("X", "")

    return bot_response

# Function to handle WordNet-based definition queries
def handle_definition_query(query):
    try:
        # Extract the word to define
        word = query.lower().replace("what is ", "").replace("define ", "").strip("?.")

        # Fetch synsets for the word
        synsets = wn.synsets(word)

        # If no synsets are found, return a user-friendly message
        if not synsets:
            return f"Sorry, I couldn't find a definition for '{word}' in my database."

        # Format multiple senses if available
        definitions = [f"{i + 1}. {synset.definition()}" for i, synset in enumerate(synsets)]
        return f"Here are the definitions for '{word}':\n" + "\n".join(definitions)
    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching definition for '{word}': {e}")
        return f"An error occurred while fetching the definition for '{word}'. Please try again."

# Function to perform sentiment analysis
def perform_sentiment_analysis(sentence):
    try:
        # Analyze sentiment using VADER
        sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
        compound_score = sentiment_scores['compound']

        # Determine sentiment based on compound score
        if compound_score >= 0.05:
            sentiment = "Positive 😊"
        elif compound_score <= -0.05:
            sentiment = "Negative 😠"
        else:
            sentiment = "Neutral 😐"

        print(f"Sentiment: {sentiment}, Compound Score: {compound_score}")
        return sentiment, compound_score
    except Exception as e:
        # Log the error for debugging
        print(f"Error performing sentiment analysis: {e}")
        return "Unknown", 0.0

# Initialize Flask app
app = Flask(__name__)

# Login credentials
VALID_USERNAME = "abdullah"
VALID_PASSWORD = "abd123"

# Route for login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return render_template('home.html')
    else:
        return """
        <script>
            alert('Invalid credentials, please try again.');
            window.location.href = '/';
        </script> """

@app.route("/get")
def get_bot_response():
    # Retrieve user query
    query = request.args.get('msg')
    print(f"User Query: {query}")  # Debugging: Print the user query

    # Handle definition queries first
    if query.lower().startswith(("what is ", "define ")):
        definition_response = handle_definition_query(query)
        return definition_response

    # Handle Neo4j-related queries
    neo4j_response = handle_neo4j_query(query)
    if neo4j_response:
        return neo4j_response

    # Handle Prolog-related queries
    prolog_response = handle_relation_query(query)
    if prolog_response:
        return prolog_response

    # Default AIML response
    bot_response = bot.respond(query)
    if not bot_response:
        bot_response = "I'm sorry, I don't understand that yet."

    # Perform sentiment analysis only if the query is related to feelings or mood
    if "feel" in query.lower() or "mood" in query.lower():
        sentiment, compound_score = perform_sentiment_analysis(query)
        print(f"Sentiment: {sentiment}, Compound Score: {compound_score}")

        # Set the last_sentiment predicate in the AIML bot
        bot.setPredicate("last_sentiment", sentiment)

        # Debugging: Print the value of last_sentiment predicate
        last_sentiment_value = bot.getPredicate("last_sentiment")
        print(f"Last Sentiment Predicate Value: {last_sentiment_value}")

        # Append sentiment analysis result to the bot response
        bot_response += f" Based on your input, your mood seems to be {sentiment}."

    # Debugging: Print final bot response
    print(f"Final Bot Response: {bot_response}")

    return bot_response



if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)


















# Find the relationship between Ali and Ahmad
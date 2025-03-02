# # from flask import Flask, request, render_template
# # from aiml import Kernel
# # from glob import glob
# # import nltk
# # from nltk.corpus import wordnet as wn
# # import pytholog as pl
# #
# # # Download required NLTK resources (only the first time)
# # nltk.download('wordnet')
# # nltk.download('omw-1.4')
# #
# # # Initialize AIML Kernel
# # bot = Kernel()
# #
# # # Load AIML files
# # aiml_files = glob("D:\\JN\\Fitness_chatbot\\*.aiml")
# # for file in aiml_files:
# #     bot.learn(file)
# #
# # # Initialize Prolog knowledge base
# # kb = pl.KnowledgeBase("fitness_kb")
# # kb.clear_cache()
# # kb.from_file(r"D:\JN\Fitness_chatbot\fitness_kb.pl")  # Ensure the correct path to the Prolog file
# #
# # # Set bot predicates
# # bot.setBotPredicate("master", "ABDULLAH")
# # bot.setBotPredicate("order", "ASSISTANT")
# # bot.setBotPredicate("name", "JARVIS")
# # bot.setPredicate("name", "Mr.ABDULLAH")
# #
# # # Initialize Flask app
# # app = Flask(__name__)
# #
# # @app.route("/")
# # def home():
# #     # Serve the chat interface
# #     return render_template("home.html")
# #
# # @app.route("/get")
# # def get_bot_response():
# #     # Retrieve user query
# #     query = request.args.get('msg')
# #     if not query:
# #         return "Please enter a message."
# #
# #     # Handle definition queries
# #     if query.lower().startswith("what is ") or query.lower().startswith("define "):
# #         word = query.lower().replace("what is ", "").replace("define ", "").strip()
# #         definition = get_definition(word)
# #         if definition:
# #             return f"Let me look it up for you. The definition of {word} is: {definition}"
# #         else:
# #             return f"Sorry, I couldn't find a definition for '{word}'."
# #
# #     # Handle coach-related queries
# #     if "who is the coach for" in query.lower():
# #         activity = query.lower().replace("who is the coach for", "").strip()
# #         coach = get_coach(activity)
# #         if coach:
# #             return f"The coach for {activity} is {coach}."
# #         else:
# #             return f"I'm sorry, I don't know the coach for {activity} yet."
# #
# #     # Handle participant-related queries
# #     if "who participates in" in query.lower():
# #         activity = query.lower().replace("who participates in", "").strip()
# #         participants = get_participants(activity)
# #         if participants:
# #             return f"Let me find the participants of {activity}. They are: {', '.join(participants)}"
# #         else:
# #             return f"I'm sorry, I don't know who participates in {activity} yet."
# #
# #     # Default AIML response
# #     bot_response = bot.respond(query)
# #     if not bot_response:
# #         bot_response = "I'm sorry, I don't understand that yet."
# #
# #     return bot_response
# #
# # def get_definition(word):
# #     """Get the definition of a word using WordNet."""
# #     synsets = wn.synsets(word)
# #     if not synsets:
# #         return None
# #     return synsets[0].definition()
# #
# # def get_coach(activity):
# #     """Get the coach for an activity from the Prolog knowledge base."""
# #     result = kb.query(pl.Expr(f"coach(Y, {activity})"))
# #     if result:
# #         return result[0].get('Y')
# #     return None
# #
# # def get_participants(activity):
# #     """Get the participants of an activity from the Prolog knowledge base."""
# #     result = kb.query(pl.Expr(f"participates(X, {activity})"))
# #     if result:
# #         return [res.get('X') for res in result]
# #     return None
# #
# # if __name__ == "__main__":
# #     # Run Flask app
# #     app.run(host="0.0.0.0", port=5000, debug=True)
#
# #
from flask import Flask, request, render_template
from aiml import Kernel
from glob import glob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
import spacy
import pytholog as pl
nltk.download('wordnet')
nltk.download('omw-1.4')
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


# def get_defi(query):
#     bot.respond(query)
#     definations =getDefinition(bot.getPredicate("rel"))
#     bot.setPredicate("definition","definations")
def getDefinition(word):
    try:
        # Try fetching the most relevant synset based on noun POS
        synsets = wn.synsets(word)
        if not synsets:
            return f"Sorry, I couldn't find a definition for '{word}'."

        # Fetch the definition of the first synset
        definition = synsets[0].definition()
        return f"The definition of '{word}' is: {definition}"
    except Exception as e:
        return f"An error occurred while fetching the definition: {str(e)}"


# Function to classify sentence type
def classify_sentence(sentence):
    tokens = word_tokenize(sentence)
    if sentence.endswith('?') or any(word.lower() in ['who', 'what', 'when', 'where', 'why', 'how'] for word in tokens):
        return "Question"
    elif sentence.endswith('!'):
        return "Exclamation"
    else:
        return "Statement"

# Function to identify pronouns and classify perspectives
def classify_pronouns(sentence):
    pronoun_perspective = {
        "first_person": {"i", "me", "my", "mine", "we", "us", "our", "ours"},
        "second_person": {"you", "your", "yours"},
        "third_person": {"he", "him", "his", "she", "her", "hers", "they", "them", "their", "theirs", "it", "its"}
    }

    # Tokenize and tag parts of speech
    tokens = word_tokenize(sentence.lower())
    pos_tags = pos_tag(tokens)

    # Filter personal pronouns
    pronouns = [word for word, tag in pos_tags if tag == "PRP" or tag == "PRP$"]

    # Classify pronouns by perspective
    classified_pronouns = {"first_person": [], "second_person": [], "third_person": []}
    for pronoun in pronouns:
        for perspective, pronoun_set in pronoun_perspective.items():
            if pronoun in pronoun_set:
                classified_pronouns[perspective].append(pronoun)

    return classified_pronouns

# Function to handle WordNet-based definition queries
def handle_definition_query(query):
    # Extract the word to define
    word = query.lower().replace("what is ", "").replace("define ", "").strip("?.")
    synsets = wn.synsets(word)

    if not synsets:
        return f"Sorry, I couldn't find a definition for '{word}'."

    # Format multiple senses if available
    definitions = [f"{i+1}. {synset.definition()}" for i, synset in enumerate(synsets)]
    return f"Here are the definitions for '{word}':\n" + "\n".join(definitions)

# Function to extract named entities using spaCy
def extract_named_entities(sentence):
    doc = nlp(sentence)
    entities = {}
    for ent in doc.ents:
        entities[ent.text] = ent.label_
    return entities

# Function to perform sentiment analysis
def perform_sentiment_analysis(sentence):
    sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
    if sentiment_scores['compound'] >= 0.05:
        return "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

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
        return render_template('HOME.html')
    else:
        return """
        <script>
            alert('Invalid credentials, please try again.');
            window.location.href = '/';
        </script> """

@app.route("/")
def home():
    # Serve the chat interface
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    # Retrieve user query
    query = request.args.get('msg')

    # Check if the query is a definition request
    if query.lower().startswith(("what is ", "define ")):
        definition_response = handle_definition_query(query)
        return definition_response

    # Perform sentiment analysis
    sentiment = perform_sentiment_analysis(query)
    bot.setPredicate("last_sentiment", sentiment)  # Save sentiment as predicate

    # Handle relation-based queries and AIML response
    bot_response = handle_relation_query(query)

    # Conditionally append sentiment analysis result if relevant
    if "mood" in query.lower() or "feel" in query.lower():
        bot_response += f" Based on your input, your mood seems to be {sentiment}."

    # Extract named entities (if needed for debugging or response construction)
    named_entities = extract_named_entities(query)
    # Optional: Log entities for debugging
    # print(f"Extracted Entities: {named_entities}")

    # Final response (without redundant mood output for non-relevant queries)
    return bot_response

    # final_response = (
    #     f"{bot_response}\n"
    #     # f"[Classified Sentence Type: {sentence_type}]\n"
    #     f"[Mood: {sentiment}]\n"
    #     # f"[Pronouns and Perspectives: {pronoun_analysis}]\n"
    #     # f"[Named Entities: {named_entities}]"
    # )

    # return final_response

if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)









# from flask import Flask, request, render_template
# from aiml import Kernel
# from glob import glob
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
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# # nltk.download('vader_lexicon')  # For sentiment analysis
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
# # Function to handle Prolog queries
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
# # Function to handle WordNet-based definition queries
# def handle_definition_query(query):
#     # Extract the word to define
#     word = query.lower().replace("what is ", "").replace("define ", "").strip("?.")
#     synsets = wn.synsets(word)
#
#     if not synsets:
#         return f"Sorry, I couldn't find a definition for '{word}'."
#
#     # Format multiple senses if available
#     definitions = [f"{i+1}. {synset.definition()}" for i, synset in enumerate(synsets)]
#     return f"Here are the definitions for '{word}':\n" + "\n".join(definitions)
#
# # Function to perform sentiment analysis
# def perform_sentiment_analysis(sentence):
#     sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
#     if sentiment_scores['compound'] >= 0.05:
#         return "Positive"
#     elif sentiment_scores['compound'] <= -0.05:
#         return "Negative"
#     else:
#         return "Neutral"
#
# # Initialize Flask app
# app = Flask(__name__)
#
# # Login credentials
# VALID_USERNAME = "abdullah"
# VALID_PASSWORD = "abd123"
#
# # Route for login page
# @app.route('/')
# def login_page():
#     return render_template('login.html')
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
#
#     # Handle Neo4j-related queries
#     neo4j_response = handle_neo4j_query(query)
#     if neo4j_response:
#         return neo4j_response
#
#     # Handle Prolog-related queries
#     prolog_response = handle_relation_query(query)
#     if prolog_response:
#         return prolog_response
#
#     # Handle definition queries
#     if query.lower().startswith(("what is ", "define ")):
#         definition_response = handle_definition_query(query)
#         return definition_response
#
#     # Perform sentiment analysis
#     sentiment = perform_sentiment_analysis(query)
#     bot.setPredicate("last_sentiment", sentiment)  # Save sentiment as predicate
#
#     # Default AIML response
#     bot_response = bot.respond(query)
#     if not bot_response:
#         bot_response = "I'm sorry, I don't understand that yet."
#
#     # Conditionally append sentiment analysis result if relevant
#     if "mood" in query.lower() or "feel" in query.lower():
#         bot_response += f" Based on your input, your mood seems to be {sentiment}."
#
#     return bot_response
#
# if __name__ == "__main__":
#     # Run Flask app
#     app.run(host="0.0.0.0", port=5000, debug=True)
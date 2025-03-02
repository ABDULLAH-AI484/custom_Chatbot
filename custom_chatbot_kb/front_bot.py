# from aiml.Kernel import Kernel
# from flask import Flask, request, render_template
# from glob import glob
#
# # Initialize AIML Kernel
# bot = Kernel()
#
# # Load AIML files during startup
# aiml_path = "D:\JN\Fitness_chatbot/*.aiml"
# files = glob(aiml_path)
# for filename in files:
#     print(f"Learning from file: {filename}")
#     bot.learn(filename)
#
# # Initialize Flask app
# app = Flask(__name__)
#
#
# @app.route("/")
# def home():
#     # Render a simple HTML home page for interaction
#     return render_template("home.html")
#
#
# @app.route("/get")
# def get_bot_response():
#     # Get the user message from query parameters
#     query = request.args.get('msg')
#
#     # Respond using AIML Kernel
#     response = bot.respond(query)
#
#     # Fallback if no response is found
#     if not response:
#         response = "I'm sorry, I don't understand that yet."
#
#     return str(response)
#
#
# if __name__ == "__main__":
#     # Run Flask app
#     app.run(host="0.0.0.0", port=5000, debug=True)

#
# from flask import Flask, request
# from aiml.Kernel import Kernel
# from glob import glob
# from nltk_practice import getDefinition
#
# # Initialize AIML Kernel
# bot = Kernel()
#
# # Load AIML files during startup
# aiml_path = "D:/JN/AIML_chatbot/pythonProject/*.aiml"
# files = glob(aiml_path)
# for filename in files:
#     print(f"Learning from file: {filename}")
#     bot.learn(filename)
#
# # Initialize Flask app
# app = Flask(__name__)
#
# # Read HTML content
# with open("home.html", "r") as file:
#     html_content = file.read()
#
# @app.route("/")
# def home():
#     # Serve the HTML content
#     return html_content
# #
# # @app.route("/get")
# # def get_bot_response():
# #     # Get the user message from query parameters
# #     query = request.args.get('msg')
# #
# #     # Respond using AIML Kernel
# #     response = bot.respond(query)
# #
# #     # Fallback if no response is found
# #     if not response:
# #         response = "I'm sorry, I don't understand that yet."
# #
#     # return str(response)
# @app.route("/get")
# def get_bot_response():
#     # Retrieve user query
#     query = request.args.get('msg')
#     if not query:
#         return "Please enter a message."
#
#     # Get the chatbot's response
#     bot_response = bot.respond(query)
#
#     # Check if a WordNet query was triggered
#     word = bot.getPredicate("word")
#     if word:
#         definition = getDefinition(word)
#         bot.setPredicate("definition", definition)
#         bot_response += f" {definition}"
#
#     # Return the response
#     return bot_response or ":)"
#
#
# if __name__ == "__main__":
#     # Run Flask app
#     app.run(host="0.0.0.0", port=5000, debug=True)

# from flask import Flask, request, jsonify
# from aiml.Kernel import Kernel
# from glob import glob
# from flask_cors import CORS  # Handle cross-origin requests
# import time
#
# # Monkey-patch aiml Kernel for Python 3.8+
# if not hasattr(time, 'clock'):  # Check if 'clock' is unavailable
#     import aiml.Kernel
#     aiml.Kernel.time = time  # Use the modern `perf_counter`
#     aiml.Kernel.time.clock = time.perf_counter
#
# # Initialize AIML Kernel
# bot = Kernel()
#
# # Load AIML files during startup
# aiml_path = "D:/JN/AIML_chatbot/pythonProject/*.aiml"
# files = glob(aiml_path)
# for filename in files:
#     print(f"Learning from file: {filename}")
#     bot.learn(filename)
#
# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
#
# # Read HTML content
# with open("home.html", "r") as file:
#     html_content = file.read()
#
# @app.route("/")
# def home():
#     # Serve the HTML content
#     return html_content
#
# @app.route("/data", methods=["POST"])
# def get_bot_response():
#     # Parse the incoming JSON request
#     data = request.json
#     query = data.get("data")  # Key matches the front-end JSON payload
#
#     # Respond using AIML Kernel
#     response = bot.respond(query)
#
#     # Fallback if no response is found
#     if not response:
#         response = "I'm sorry, I don't understand that yet."
#
#     return jsonify({"response": True, "message": response})
#
# if __name__ == "__main__":
#     # Run Flask app
#     app.run(host="0.0.0.0", port=5000, debug=True)




# from flask import Flask, request,jsonify, render_template_string
# from aiml import Kernel
# from glob import glob
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk import pos_tag, ne_chunk
# from nltk.corpus import wordnet as wn
# from nltk.tree import Tree
# from nltk.sentiment import SentimentIntensityAnalyzer
#
# # Initialize Flask app
# app = Flask(__name__)
#
# # Initialize AIML Kernel
# bot = Kernel()
# aiml_files = glob("D:/JN/AIML_chatbot/pythonProject/*.aiml")
# for file in aiml_files:
#     bot.learn(file)
#
# # Initialize Sentiment Analyzer
# nltk.download('vader_lexicon')
# sentiment_analyzer = SentimentIntensityAnalyzer()
#
# # Initialize NLTK resources
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
#
# # Dictionary to store context entities
# context_entities = {}
#
# # Function Definitions (from your code)
# def classify_sentence(sentence):
#     tokens = word_tokenize(sentence)
#     if sentence.endswith('?') or any(word.lower() in ['who', 'what', 'when', 'where', 'why', 'how'] for word in tokens):
#         return "Question"
#     elif sentence.endswith('!'):
#         return "Exclamation"
#     else:
#         return "Statement"
#
# def classify_pronouns(sentence):
#     pronoun_perspective = {
#         "first_person": {"i", "me", "my", "mine", "we", "us", "our", "ours"},
#         "second_person": {"you", "your", "yours"},
#         "third_person": {"he", "him", "his", "she", "her", "hers", "they", "them", "their", "theirs", "it", "its"}
#     }
#     tokens = word_tokenize(sentence.lower())
#     pos_tags = pos_tag(tokens)
#     pronouns = [word for word, tag in pos_tags if tag == "PRP" or tag == "PRP$"]
#     classified_pronouns = {"first_person": [], "second_person": [], "third_person": []}
#     for pronoun in pronouns:
#         for perspective, pronoun_set in pronoun_perspective.items():
#             if pronoun in pronoun_set:
#                 classified_pronouns[perspective].append(pronoun)
#     return classified_pronouns
#
# def handle_definition_query(query):
#     word = query.lower().replace("what is ", "").replace("define ", "").strip("?.")
#     synsets = wn.synsets(word)
#     if not synsets:
#         return f"Sorry, I couldn't find a definition for '{word}'."
#     definitions = [f"{i+1}. {synset.definition()}" for i, synset in enumerate(synsets)]
#     return f"Here are the definitions for '{word}':\n" + "\n".join(definitions)
#
# def extract_named_entities(sentence):
#     tokens = word_tokenize(sentence)
#     pos_tags = pos_tag(tokens)
#     named_entities = ne_chunk(pos_tags)
#     entities = {}
#     for chunk in named_entities:
#         if isinstance(chunk, Tree):
#             entity_name = " ".join(c[0] for c in chunk)
#             entity_type = chunk.label()
#             entities[entity_name] = entity_type
#     return entities
#
# def answer_named_entity_query(query, context_entities):
#     query = query.lower()
#     for entity, entity_type in context_entities.items():
#         if entity.lower() in query:
#             if entity_type == "PERSON":
#                 return f"{entity} is a PERSON in the given context."
#             elif entity_type == "ORGANIZATION":
#                 return f"{entity} is an ORGANIZATION in the given context."
#             elif entity_type == "GPE":
#                 return f"{entity} is a LOCATION (geopolitical entity) in the given context."
#             elif entity_type == "DATE":
#                 return f"{entity} represents a DATE in the given context."
#     return "I'm not sure how to answer that based on the context."
#
# def perform_sentiment_analysis(sentence):
#     sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
#     if sentiment_scores['compound'] >= 0.05:
#         return "Positive"
#     elif sentiment_scores['compound'] <= -0.05:
#         return "Negative"
#     else:
#         return "Neutral"
#
# # Route for chatbot home
# @app.route("/")
# def home():
#     return render_template_string("""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Chatbot</title>
#         <script>
#             function sendMessage() {
#                 let userInput = document.getElementById("userInput").value;
#                 fetch(`/get?msg=${encodeURIComponent(userInput)}`)
#                     .then(response => response.json())
#                     .then(data => {
#                         let chatBox = document.getElementById("chatBox");
#                         chatBox.innerHTML += `<p><b>You:</b> ${userInput}</p>`;
#                         chatBox.innerHTML += `<p><b>Bot:</b> ${data.response}</p>`;
#                         document.getElementById("userInput").value = "";
#                     });
#             }
#         </script>
#     </head>
#     <body>
#         <div id="chatBox" style="border:1px solid black; padding:10px; height:300px; overflow:auto;"></div>
#         <input type="text" id="userInput" />
#         <button onclick="sendMessage()">Send</button>
#     </body>
#     </html>
#     """)
#
# # Route to get bot response
# @app.route("/get")
# def get_bot_response():
#     user_input = request.args.get('msg', '')
#     if not user_input:
#         return jsonify({"response": "Please enter a message."})
#
#     sentence_type = classify_sentence(user_input)
#     sentiment = perform_sentiment_analysis(user_input)
#     pronouns = classify_pronouns(user_input)
#
#     if user_input.lower().startswith(("what is ", "define ")):
#         bot_response = handle_definition_query(user_input)
#     else:
#         named_entities = extract_named_entities(user_input)
#         context_entities.update(named_entities)
#         if "who is " in user_input.lower() or "what is " in user_input.lower():
#             bot_response = answer_named_entity_query(user_input, context_entities)
#         else:
#             bot_response = bot.respond(user_input) or "I'm sorry, I don't understand that yet."
#
#     return jsonify({
#         "response": bot_response,
#         "sentence_type": sentence_type,
#         "sentiment": sentiment,
#         "pronouns": pronouns,
#         "named_entities": context_entities
#     })
#
# if __name__ == "__main__":
#     app.run(debug=True)







from flask import Flask, request
from aiml import Kernel
from glob import glob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
import spacy
import pytholog as pl

# Download required NLTK resources (only the first time)
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize AIML Kernel
bot = Kernel()

# Load AIML files
aiml_files = glob("D:\\JN\\Fitness_chatbot\\*.aiml")
for file in aiml_files:
    bot.learn(file)

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

# Function to answer NER-based questions
def answer_named_entity_query(query, context_entities):
    query = query.lower()

    # Check if query relates to a known entity
    for entity, entity_type in context_entities.items():
        if entity.lower() in query:
            if entity_type == "PERSON":
                return f"{entity} is a PERSON in the given context."
            elif entity_type == "ORG":
                return f"{entity} is an ORGANIZATION in the given context."
            elif entity_type == "GPE":
                return f"{entity} is a LOCATION (geopolitical entity) in the given context."
            elif entity_type == "DATE":
                return f"{entity} represents a DATE in the given context."

    return "I'm not sure how to answer that based on the context."

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

    # Debug: Print the relation and entity
    print(f"Debug: Relation = {relation}, Entity = {entity}")

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

# Read HTML content
with open("home.html", "r") as file:
    html_content = file.read()

@app.route("/")
def home():
    # Serve the HTML content
    return html_content

@app.route("/get")
def get_bot_response():
    # Retrieve user query
    query = request.args.get('msg')
    if not query:
        return "Please enter a message."

    # Get the chatbot's response
    bot_response = bot.respond(query)

    # Fallback if no response is found
    if not bot_response:
        bot_response = "I'm sorry, I don't understand that yet."

    # Return the response as plain text
    return str(bot_response)

    # Classify the sentence type
    sentence_type = classify_sentence(query)
    bot.setPredicate("last_sentence_type", sentence_type)  # Save sentence type as predicate

    # Perform sentiment analysis
    sentiment = perform_sentiment_analysis(query)
    bot.setPredicate("last_sentiment", sentiment)  # Save sentiment as predicate

    # Identify pronouns and their perspectives
    pronoun_analysis = classify_pronouns(query)
    bot.setPredicate("last_pronouns", str(pronoun_analysis))  # Save pronouns as predicate

    # Check for definition-based queries
    if query.lower().startswith(("what is ", "define ")):
        bot_response = handle_definition_query(query)
    else:
        # Extract named entities and store them for context
        named_entities = extract_named_entities(query)
        context_entities = named_entities
        bot.setPredicate("last_entities", str(named_entities))  # Save named entities as predicate

        # Check for NER-based queries (e.g., "Who is Tim Cook?")
        if "who is " in query.lower() or "what is " in query.lower():
            bot_response = answer_named_entity_query(query, context_entities)
        else:
            # Get AIML response
            bot_response = bot.respond(query)

            # Check if the response triggered a relation query
            relation = bot.getPredicate("rel")
            if relation:
                bot_response = handle_relation_query(query)  # Handle the relation-based query

    # Retrieve last sentence type, mood, and pronouns for dynamic response
    last_sentence_type = bot.getPredicate("last_sentence_type")
    last_sentiment = bot.getPredicate("last_sentiment")
    last_pronouns = bot.getPredicate("last_pronouns")

    # Return the AIML bot response along with additional information
    response = {
        "bot_response": bot_response,
        "sentence_type": last_sentence_type,
        "sentiment": last_sentiment,
        "pronouns": last_pronouns,
        "named_entities": context_entities
    }

    return response

if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)



# from nltk.sentiment import SentimentIntensityAnalyzer  # For Sentiment Analysis
# from aiml import Kernel  # AIML Kernel
# import pytholog as pl  # Prolog integration
# from glob import glob
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk import pos_tag, ne_chunk
# from nltk.corpus import wordnet as wn
# from nltk.tree import Tree
#
# # Download required NLTK resources (only the first time)
# nltk.download('vader_lexicon')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt_tab')
# nltk.download('maxent_ne_chunker_tab')
# nltk.download('words')
#
# # Initialize AIML bot
# bot = Kernel()
#
# # Load AIML files
# aiml_files = glob("D:\\JN\\Fitness_chatbot\\*.aiml")
# for file in aiml_files:
#     bot.learn(file)
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
# # Function to classify sentence type
# def classify_sentence(sentence):
#     tokens = word_tokenize(sentence)
#     if sentence.endswith('?') or any(word.lower() in ['who', 'what', 'when', 'where', 'why', 'how'] for word in tokens):
#         return "Question"
#     elif sentence.endswith('!'):
#         return "Exclamation"
#     else:
#         return "Statement"
#
# # Function to identify pronouns and classify perspectives
# def classify_pronouns(sentence):
#     pronoun_perspective = {
#         "first_person": {"i", "me", "my", "mine", "we", "us", "our", "ours"},
#         "second_person": {"you", "your", "yours"},
#         "third_person": {"he", "him", "his", "she", "her", "hers", "they", "them", "their", "theirs", "it", "its"}
#     }
#
#     # Tokenize and tag parts of speech
#     tokens = word_tokenize(sentence.lower())
#     pos_tags = pos_tag(tokens)
#
#     # Filter personal pronouns
#     pronouns = [word for word, tag in pos_tags if tag == "PRP" or tag == "PRP$"]
#
#     # Classify pronouns by perspective
#     classified_pronouns = {"first_person": [], "second_person": [], "third_person": []}
#     for pronoun in pronouns:
#         for perspective, pronoun_set in pronoun_perspective.items():
#             if pronoun in pronoun_set:
#                 classified_pronouns[perspective].append(pronoun)
#
#     return classified_pronouns
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
# # Function to extract named entities using nltk.ne_chunk
# def extract_named_entities(sentence):
#     tokens = word_tokenize(sentence)
#     pos_tags = pos_tag(tokens)
#     named_entities = ne_chunk(pos_tags)
#
#     # Extract named entities from the chunked tree
#     entities = {}
#     for chunk in named_entities:
#         if isinstance(chunk, Tree):
#             entity_name = " ".join(c[0] for c in chunk)  # Join the words in the chunk
#             entity_type = chunk.label()  # Get the entity type (e.g., PERSON, ORGANIZATION)
#             # Skip irrelevant tokens like "THE" and "FOR"
#             if entity_name.lower() not in {"the", "for", "is", "a", "an", "coach for"}:
#                 entities[entity_name] = entity_type
#
#     return entities
#
# # Function to answer NER-based questions
# def answer_named_entity_query(query, context_entities):
#     query = query.lower()
#
#     # Check if query relates to a known entity
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
#
#     return "I'm not sure how to answer that based on the context."
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
# # Function to handle relation-based queries using AIML and Prolog
# # Function to handle relation-based queries using AIML and Prolog
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
#     # Debug: Print the relation and entity
#     print(f"Debug: Relation = {relation}, Entity = {entity}")
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
# # Main program loop for user input
# print("Ask anything, and I will classify your sentence type, mood, pronouns, definitions, and named entities!")
# print("Type 'bye' to exit.")
#
# # Dictionary to store named entities for context
# context_entities = {}
#
# while True:
#     # Clear named entities at the start of each interaction
#     context_entities.clear()
#
#     # Get user input
#     user_input = input("\nYou: ").strip()
#
#     # Exit condition
#     if user_input.lower() == "bye":
#         print("Goodbye!")
#         break
#
#     # Classify the sentence type
#     sentence_type = classify_sentence(user_input)
#     bot.setPredicate("last_sentence_type", sentence_type)  # Save sentence type as predicate
#
#     # Perform sentiment analysis
#     sentiment = perform_sentiment_analysis(user_input)
#     bot.setPredicate("last_sentiment", sentiment)  # Save sentiment as predicate
#
#     # Identify pronouns and their perspectives
#     pronoun_analysis = classify_pronouns(user_input)
#     bot.setPredicate("last_pronouns", str(pronoun_analysis))  # Save pronouns as predicate
#
#     # Check for definition-based queries
#     if user_input.lower().startswith(("what is ", "define ")):
#         bot_response = handle_definition_query(user_input)
#     else:
#         # Extract named entities and store them for context
#         named_entities = extract_named_entities(user_input)
#         context_entities.update(named_entities)
#         bot.setPredicate("last_entities", str(named_entities))  # Save named entities as predicate
#
#         # Check for NER-based queries (e.g., "Who is Tim Cook?")
#         if "who is " in user_input.lower() or "what is " in user_input.lower():
#             bot_response = answer_named_entity_query(user_input, context_entities)
#         else:
#             # Get AIML response
#             bot_response = bot.respond(user_input)
#
#             # Check if the response triggered a relation query
#             relation = bot.getPredicate("rel")
#             if relation:
#                 bot_response = handle_relation_query(user_input)  # Handle the relation-based query
#
#     # Retrieve last sentence type, mood, and pronouns for dynamic response
#     last_sentence_type = bot.getPredicate("last_sentence_type")
#     last_sentiment = bot.getPredicate("last_sentiment")
#     last_pronouns = bot.getPredicate("last_pronouns")
#
#     # Display the AIML bot response, classified sentence type, mood, pronoun perspectives, and named entities
#     print(f"Bot: {bot_response}")
#     print(f"[Classified Sentence Type: {last_sentence_type}]")
#     print(f"[Mood: {last_sentiment}]")
#     print(f"[Pronouns and Perspectives: {last_pronouns}]")
#     print(f"[Named Entities: {context_entities}]")


from flask import Flask, request, render_template, redirect, url_for, session
import os
import aiml
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
import spacy
import pytholog as pl
from autocorrect import Speller
import nltk

# Download required NLTK resources
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session management

# Brain file path
BRAIN_FILE = "./pretrained_model/aiml_pretrained_model.dump"

# Initialize AIML Kernel
bot = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    bot.loadBrain(BRAIN_FILE)
else:
    print("Parsing AIML files")
    bot.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
    print("Saving brain file: " + BRAIN_FILE)
    bot.saveBrain(BRAIN_FILE)

# Initialize Prolog knowledge base
kb = pl.KnowledgeBase("fitness_kb")
kb.clear_cache()
kb.from_file(r"D:\JN\Fitness_chatbot\fitness_kb.pl")  # Update the path to your Prolog file

# Set bot predicates
bot.setBotPredicate("master", "ABDULLAH")
bot.setBotPredicate("order", "ASSISTANT")
bot.setBotPredicate("name", "JARVIS")
bot.setPredicate("name", "Mr.ABDULLAH")

# Initialize NLP tools
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = SentimentIntensityAnalyzer()
spell = Speller(lang="en")


# Function to classify sentences
def classify_sentence(sentence):
    tokens = word_tokenize(sentence)
    if sentence.endswith('?') or any(word.lower() in ['who', 'what', 'when', 'where', 'why', 'how'] for word in tokens):
        return "Question"
    elif sentence.endswith('!'):
        return "Exclamation"
    else:
        return "Statement"


# Function to perform sentiment analysis
def perform_sentiment_analysis(sentence):
    sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
    if sentiment_scores['compound'] >= 0.05:
        return "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"


# Function to handle definition queries using WordNet
def handle_definition_query(query):
    word = query.lower().replace("what is ", "").replace("define ", "").strip("?.")
    synsets = wn.synsets(word)
    if not synsets:
        return f"Sorry, I couldn't find a definition for '{word}'."
    definitions = [f"{i+1}. {synset.definition()}" for i, synset in enumerate(synsets)]
    return f"Here are the definitions for '{word}':\n" + "\n".join(definitions)


# Function to query Prolog knowledge base
def query_prolog(relation, entity):
    expr = f"{relation}(Y, {entity})"
    results = kb.query(pl.Expr(expr))
    if results:
        return list(set([result.get('Y') for result in results]))
    return None


# Function to handle relation-based queries
def handle_relation_query(user_input):
    bot_response = bot.respond(user_input)
    relation = bot.getPredicate("rel")
    entity = bot.getPredicate("X")
    if relation and entity:
        result = query_prolog(relation, entity)
        if result:
            result_str = ", ".join(result)
            bot.setPredicate("Y", result_str)
            bot_response += f"\n[Prolog Result: {result_str}]"
        else:
            bot.setPredicate("Y", "unknown")
            bot_response += "\n[Prolog Result: No information found.]"
        bot.setPredicate("rel", "")
        bot.setPredicate("X", "")
    return bot_response


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "password":  # Dummy credentials
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"
            return render_template("login.html", error=error)
    return render_template("login.html")


# Logout route
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


# Home route (protected)
@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    if not session.get("logged_in"):
        return "Unauthorized access. Please log in."

    query = request.args.get('msg')
    if not query:
        return "Please enter a message."

    # Spell correction
    query = " ".join([spell(w) for w in query.split()])

    # Check for definition queries
    if query.lower().startswith(("what is ", "define ")):
        return handle_definition_query(query)

    # Handle relation-based queries and AIML response
    bot_response = handle_relation_query(query)

    # Perform sentence classification and sentiment analysis
    sentence_type = classify_sentence(query)
    sentiment = perform_sentiment_analysis(query)

    final_response = (
        f"{bot_response}\n"
        f"[Classified Sentence Type: {sentence_type}]\n"
        f"[Mood: {sentiment}]"
    )
    return final_response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

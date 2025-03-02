# from flask import Flask, request, render_template
# from aiml import Kernel
# from glob import glob
# import nltk
# from nltk.corpus import wordnet as wn
# import pytholog as pl
#
# # Download required NLTK resources (only the first time)
# nltk.download('wordnet')
# nltk.download('omw-1.4')
#
# # Initialize AIML Kernel
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
# # Initialize Flask app
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#     # Serve the chat interface
#     return render_template("home.html")
#
# @app.route("/get")
# def get_bot_response():
#     # Retrieve user query
#     query = request.args.get('msg')
#     if not query:
#         return "Please enter a message."
#
#     # Handle definition queries
#     if query.lower().startswith("what is ") or query.lower().startswith("define "):
#         word = query.lower().replace("what is ", "").replace("define ", "").strip()
#         definition = get_definition(word)
#         if definition:
#             return f"Let me look it up for you. The definition of {word} is: {definition}"
#         else:
#             return f"Sorry, I couldn't find a definition for '{word}'."
#
#     # Handle coach-related queries
#     if "who is the coach for" in query.lower():
#         activity = query.lower().replace("who is the coach for", "").strip()
#         coach = get_coach(activity)
#         if coach:
#             return f"The coach for {activity} is {coach}."
#         else:
#             return f"I'm sorry, I don't know the coach for {activity} yet."
#
#     # Handle participant-related queries
#     if "who participates in" in query.lower():
#         activity = query.lower().replace("who participates in", "").strip()
#         participants = get_participants(activity)
#         if participants:
#             return f"Let me find the participants of {activity}. They are: {', '.join(participants)}"
#         else:
#             return f"I'm sorry, I don't know who participates in {activity} yet."
#
#     # Default AIML response
#     bot_response = bot.respond(query)
#     if not bot_response:
#         bot_response = "I'm sorry, I don't understand that yet."
#
#     return bot_response
#
# def get_definition(word):
#     """Get the definition of a word using WordNet."""
#     synsets = wn.synsets(word)
#     if not synsets:
#         return None
#     return synsets[0].definition()
#
# def get_coach(activity):
#     """Get the coach for an activity from the Prolog knowledge base."""
#     result = kb.query(pl.Expr(f"coach(Y, {activity})"))
#     if result:
#         return result[0].get('Y')
#     return None
#
# def get_participants(activity):
#     """Get the participants of an activity from the Prolog knowledge base."""
#     result = kb.query(pl.Expr(f"participates(X, {activity})"))
#     if result:
#         return [res.get('X') for res in result]
#     return None
#
# if __name__ == "__main__":
#     # Run Flask app
#     app.run(host="0.0.0.0", port=5000, debug=True)


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

@app.route("/")
def home():
    # Serve the chat interface
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    # Retrieve user query
    query = request.args.get('msg')
    if not query:
        return "Please enter a message."

    # Classify the sentence type
    sentence_type = classify_sentence(query)

    # Perform sentiment analysis
    sentiment = perform_sentiment_analysis(query)

    # Identify pronouns and their perspectives
    pronoun_analysis = classify_pronouns(query)

    # Extract named entities
    named_entities = extract_named_entities(query)

    # Handle definition queries
    if query.lower().startswith(("what is ", "define ")):
        word = query.lower().replace("what is ", "").replace("define ", "").strip("?.")
        synsets = wn.synsets(word)
        if not synsets:
            bot_response = f"Sorry, I couldn't find a definition for '{word}'."
        else:
            definitions = [f"{i+1}. {synset.definition()}" for i, synset in enumerate(synsets)]
            bot_response = f"Here are the definitions for '{word}':\n" + "\n".join(definitions)
    else:
        # Handle coach-related queries
        if "who is the coach for" in query.lower():
            activity = query.lower().replace("who is the coach for", "").strip()
            coach = query_prolog("coach", activity)
            if coach:
                bot_response = f"The coach for {activity} is {', '.join(coach)}."
            else:
                bot_response = f"I'm sorry, I don't know the coach for {activity} yet."
        # Handle participant-related queries
        elif "who participates in" in query.lower():
            activity = query.lower().replace("who participates in", "").strip()
            participants = query_prolog("participates", activity)
            if participants:
                bot_response = f"Let me find the participants of {activity}. They are: {', '.join(participants)}"
            else:
                bot_response = f"I'm sorry, I don't know who participates in {activity} yet."
        else:
            # Default AIML response
            bot_response = bot.respond(query)
            if not bot_response:
                bot_response = "I'm sorry, I don't understand that yet."

    # Prepare the final response
    final_response = (
        f"{bot_response}\n"
        f"[Classified Sentence Type: {sentence_type}]\n"
        f"[Mood: {sentiment}]\n"
        f"[Pronouns and Perspectives: {pronoun_analysis}]\n"
        f"[Named Entities: {named_entities}]"
    )

    return final_response

if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
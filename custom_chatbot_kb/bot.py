from nltk.sentiment import SentimentIntensityAnalyzer  # For Sentiment Analysis
from aiml import Kernel  # AIML Kernel
import pytholog as pl  # Prolog integration
from glob import glob
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
import spacy  # Import spaCy

# Download required NLTK resources (only the first time)
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize AIML bot
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

# Main program loop for user input
print("Ask anything, and I will classify your sentence type, mood, pronouns, definitions, and named entities!")
print("Type 'bye' to exit.")

# Dictionary to store named entities for context
context_entities = {}

while True:
    # Clear named entities at the start of each interaction
    context_entities.clear()

    # Get user input
    user_input = input("\nYou: ").strip()

    # Exit condition
    if user_input.lower() == "bye":
        print("Goodbye!")
        break

    # Classify the sentence type
    sentence_type = classify_sentence(user_input)
    bot.setPredicate("last_sentence_type", sentence_type)  # Save sentence type as predicate

    # Perform sentiment analysis
    sentiment = perform_sentiment_analysis(user_input)
    bot.setPredicate("last_sentiment", sentiment)  # Save sentiment as predicate

    # Identify pronouns and their perspectives
    pronoun_analysis = classify_pronouns(user_input)
    bot.setPredicate("last_pronouns", str(pronoun_analysis))  # Save pronouns as predicate

    # Check for definition-based queries
    if user_input.lower().startswith(("what is ", "define ")):
        bot_response = handle_definition_query(user_input)
    else:
        # Extract named entities and store them for context
        named_entities = extract_named_entities(user_input)
        context_entities.update(named_entities)
        bot.setPredicate("last_entities", str(named_entities))  # Save named entities as predicate

        # Check for NER-based queries (e.g., "Who is Tim Cook?")
        if "who is " in user_input.lower() or "what is " in user_input.lower():
            bot_response = answer_named_entity_query(user_input, context_entities)
        else:
            # Get AIML response
            bot_response = bot.respond(user_input)

            # Check if the response triggered a relation query
            relation = bot.getPredicate("rel")
            if relation:
                bot_response = handle_relation_query(user_input)  # Handle the relation-based query

    # Retrieve last sentence type, mood, and pronouns for dynamic response
    last_sentence_type = bot.getPredicate("last_sentence_type")
    last_sentiment = bot.getPredicate("last_sentiment")
    last_pronouns = bot.getPredicate("last_pronouns")

    # Display the AIML bot response, classified sentence type, mood, pronoun perspectives, and named entities
    print(f"Bot: {bot_response}")
    print(f"[Classified Sentence Type: {last_sentence_type}]")
    print(f"[Mood: {last_sentiment}]")
    print(f"[Pronouns and Perspectives: {last_pronouns}]")
    print(f"[Named Entities: {context_entities}]")
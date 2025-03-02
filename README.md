# Custom Chatbot - Gym &amp; Fitness Knowledge Bot 🤖💪
Welcome to Custom Chatbot, a specialized Gym and Fitness Knowledge Bot designed to provide detailed information and answers related to fitness, exercises, and gym routines. Unlike a personal assistant, this chatbot focuses on delivering accurate and structured knowledge using advanced technologies like Prolog, Neo4j, AIML, and NLTK. Whether you're a fitness enthusiast, a gym-goer, or a trainer, this bot is here to help you with fitness-related queries and knowledge management.
### Key Features
Fitness Knowledge Base:
Uses Prolog to store and query fitness-related knowledge (e.g., exercises, muscle groups, workout plans).
Example: "who is coaches for yoga and who participates in yoga?"

Relationship Management with Neo4j:
Manages relationships between users, trainers, and gyms using Neo4j.
Example: "John is a trainer of Alice" → Stores and retrieves relationships.

Natural Language Processing (NLP):
Leverages NLTK and spaCy for tokenization, POS tagging, and understanding user queries.
Example: "Define deadlift" → Provides a detailed definition.

WordNet Integration:
Provides definitions for fitness-related terms using WordNet.
Example: "What is a deadlift?" → "A weightlifting exercise where a loaded barbell is lifted off the ground."

AIML for Structured Conversations:
Uses AIML to handle structured conversations and predefined fitness-related queries.
Example: "i want to improve my health"

Sentiment Analysis:
Uses VADER from NLTK to analyze user mood and provide empathetic responses.
Example: "I feel tired today" → "Your mood seems Negative 😠. Here’s a light workout suggestion."

User Authentication:
Simple login system to authenticate users and protect access to the chatbot.

Interactive Web Interface:
Built with Flask for a user-friendly web interface.
Users can interact with the chatbot via a web browser.
### How It Works
User Interaction:
Users interact with the chatbot through a web interface.
Queries can range from fitness advice, workout plans, definitions, or general knowledge.
Query Handling:
The chatbot processes user queries using AIML for structured conversations.
For fitness-specific queries, it uses Prolog and Neo4j to retrieve relevant information.
Knowledge Base:
Fitness-related data is stored in a Prolog knowledge base and Neo4j graph database.
Example: "What are the best exercises for chest?" → Queries Prolog for chest exercises.
Response Generation:
The chatbot combines responses from AIML, Prolog, and Neo4j to provide accurate and helpful answers.
Technologies Used
Python: Core programming language.
Flask: Web framework for the chatbot interface.
AIML: Artificial Intelligence Markup Language for structured conversations.
Prolog: Logic programming for fitness knowledge base.
Neo4j: Graph database for managing relationships.
NLTK: Natural Language Toolkit for NLP tasks.
spaCy: Advanced NLP for tokenization and POS tagging.
WordNet: Lexical database for definitions.
VADER: Sentiment analysis tool.

# # from flask import Flask, render_template, request
# import aiml
# import pytholog as pl
# from glob import glob
#
# k = aiml.Kernel()
# aimlfiles = glob(r"D:\JN\Fitness_chatbot\*.aiml")
# kb = pl.KnowledgeBase("fitness_kb")
# kb.clear_cache()
# kb.from_file(r"D:\JN\Fitness_chatbot\*.pl")
#
# for file in aimlfiles:
#     k.learn(str(file))
#
# k.setBotPredicate("master", "HAMZA")
# k.setBotPredicate("order", "ASSISTANT")
# k.setBotPredicate("name", "JARVIS")
# k.setPredicate("name", "SYED M HAMZA")
#
#
# def Person(x, relation):
#     expr = f"{relation}({x}, Y)"  # Construct Prolog query
#     results = kb.query(pl.Expr(expr))
#     if results:
#         return results[0].get('Y', None)
#     else:
#         print(f"No results found for query: {expr}")
#         return None
#
#
# def Get_relation(quer):
#     k.respond(quer)
#     relation = k.getPredicate("relation")  # "relation" should already be set by AIML
#     x = k.getPredicate("entity")  # "entity" should already be set by AIML
#
#     # Debugging: Ensure values were correctly retrieved
#     print(f"Relation: {relation}, Entity: {x}")
#
#     if not relation or not x:
#         print("Error: Missing relation or entity in AIML predicates.")
#         return
#
#     # Query Prolog using the retrieved relation and entity
#     Y = Person(x, relation)
#
#     if Y:
#         # Store the result back in AIML
#         k.setPredicate("result", Y)  # "result" will store the Prolog query result
#         print(f"Set result in AIML: {Y}")
#     else:
#         print(f"No relation found for {relation} of {x}.")
#         k.setPredicate("result", "unknown")  # Set "unknown" if no result is found
#
#
# if __name__ == "__main__":
#     print("Chatbot is running. Type 'exit' to stop.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'exit':
#             print("Exiting the chatbot.")
#             break
#
#             # Use the AIML kernel to get a response; this could trigger relation setting.
#         response = k.respond(user_input)
#         print(f"Chatbot: {response}")
#
#         # After responding, check if there are predicates set by AIML related to relations
#         relation = k.getPredicate("relation")
#         if relation:
#             Get_relation(user_input)  # Call to handle the relation-based query
#
#         # Output the result stored by Get_relation
#         result = k.getPredicate("result")
#         if result:
#             print(f"Chatbot Result: {result}")








import aiml
import pytholog as pl
from glob import glob

# Initialize AIML kernel
k = aiml.Kernel()
aimlfiles = glob(r"D:\JN\Fitness_chatbot\*.aiml")

# Initialize Prolog knowledge base
kb = pl.KnowledgeBase("fitness_kb")
kb.clear_cache()
kb.from_file(r"D:\JN\Fitness_chatbot\fitness_kb.pl")  # Ensure the correct path to the Prolog file

# Load AIML files
for file in aimlfiles:
    k.learn(str(file))

# Set bot predicates
k.setBotPredicate("master", "ABDULLAH")
k.setBotPredicate("order", "ASSISTANT")
k.setBotPredicate("name", "JARVIS")
k.setPredicate("name", "Mr.ABDULLAH")


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


def handle_relation_query(user_input):
    """Handle relation-based queries using AIML and Prolog."""
    # Respond to the user input to set AIML predicates
    k.respond(user_input)

    # Retrieve the relation and entity from AIML predicates
    relation = k.getPredicate("rel")
    entity = k.getPredicate("X")

    if not relation or not entity:
        print("Error: Missing relation or entity in AIML predicates.")
        return

    # Query Prolog using the retrieved relation and entity
    result = query_prolog(relation, entity)

    if result:
        # Convert the list of results to a comma-separated string
        result_str = ", ".join(result)
        # Store the result back in AIML
        k.setPredicate("Y", result_str)  # "Y" will store the Prolog query result as a string
    else:
        print(f"No relation found for {relation} of {entity}.")
        k.setPredicate("Y", "unknown")  # Set "unknown" if no result is found


if __name__ == "__main__":
    print("Chatbot is running. Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting the chatbot.")
            break

        # Use the AIML kernel to get a response
        response = k.respond(user_input)
        print(f"Chatbot: {response}")

        # Check if the response triggered a relation query
        relation = k.getPredicate("rel")
        if relation:
            handle_relation_query(user_input)  # Handle the relation-based query

        # Output the result stored by handle_relation_query
        result = k.getPredicate("Y")
        if result:
            print(f"Chatbot Result: {result}")
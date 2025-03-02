from neo4j import GraphDatabase

# Connect to the Neo4j database
uri = "bolt://localhost:7687"  # URL of your Neo4j instance
username = "neo4j"  # Your Neo4j username
password = "23704300"  # Your Neo4j password (default is "neo4j", change if you've updated it)

driver = GraphDatabase.driver(uri, auth=(username, password))

# def create_node_with_attributes(p_name, p_age):
#     # Open a session
#     with driver.session() as session:
#         # Cypher query to create a node with attributes
#         cypher_query = """
#         CREATE (n:Person {name: $n, age: $a})
#         """
#         # Run the query with parameters
#         session.run(cypher_query, n=p_name, a=p_age)
#
# # Call the function to create a node with name and age attributes
# create_node_with_attributes("Alice", 30)
#
# # Close the driver connection
# driver.close()

# def create_friendship(p1_name, p2_name, relationship_name):
#     # Open a session
#     with driver.session() as session:
#         # Cypher query to create a relationship between two nodes with the given names
#         cypher_query = f"""
#         MERGE (p1:Person {{name: $p1_name}})
#         MERGE (p2:Person {{name: $p2_name}})
#         MERGE (p1)-[r:{relationship_name}]->(p2)
#         RETURN p1, p2, r
#         """
#         # Run the query with parameters
#         session.run(cypher_query, p1_name=p1_name, p2_name=p2_name)
#
# # Call the function to create a friendship relationship
# create_friendship("Alice", "Bob", "is_friend_of")
#
# # Close the driver connection
# driver.close()

# def create_friendship(p1_name, p2_name, relationship_type):
#     with driver.session() as session:
#         cypher_query = f"""
#         MATCH (p1:Person {{name: $p1_name}}), (p2:Person {{name: $p2_name}})
#         MERGE (p1)-[r:{relationship_type}]->(p2)
#         """
#         session.run(cypher_query, p1_name=p1_name, p2_name=p2_name)
#
# create_friendship("Alice", "Bob", "IS_FRIEND_OF")
# def find_friends(p1_name):
#     with driver.session() as session:
#         cypher_query = """
#         MATCH (p1:Person {name: $p1_name})-[r]->(p2:Person)
#         RETURN p2.name AS friend_name
#         """
#         result = session.run(cypher_query, p1_name=p1_name)
#         friends = [record["friend_name"] for record in result]
#         return friends
#
# friends_of_alice = find_friends("Alice")
# print(friends_of_alice)


def create_node_with_attributes(p_name, p_age):
    # Open a session
    with driver.session() as session:
        # Cypher query to create a node with attributes
        cypher_query = """
        CREATE (n:Person {name: $n, age: $a})
        """
        # Run the query with parameters
        session.run(cypher_query, n=p_name, a=p_age)


# Call the function to create a node with name and age attributes
# create_node_with_attributes("Mr Abdullah", 22)

def create_friendship(p1_name, p2_name, relationship_name):
    # Open a session
    with driver.session() as session:
        # Cypher query to create a relationship between two nodes with the given names
        cypher_query = (
            "MERGE (p1:Person {name: $p1_name}) "
            "MERGE (p2:Person {name: $p2_name}) "
            f"MERGE (p1)-[r:{relationship_name}]->(p2) "
            "RETURN p1, p2, r"
        )
        # Run the query with parameters
        session.run(cypher_query, p1_name=p1_name, p2_name=p2_name)



# Call the function to create a friendship relationship
# create_friendship("Alice", "Abdullah", "is_student_of")

def find_friends(p1_name, relationship_type):
    # Open a session
    with driver.session() as session:
        # Cypher query to find all persons who are related to p1 with the given relationship type
        cypher_query = (
            "MATCH (p1:Person)-[r]->(p2:Person) "
            "WHERE p1.name = $p1_name AND type(r) = $relationship_type "
            "RETURN p2.name AS friend_name"
        )
        # Run the query with parameters and collect the results
        result = session.run(cypher_query, p1_name=p1_name, relationship_type=relationship_type)

        # Collect the names of p2 (friends)
        friends = [record["friend_name"] for record in result]

        return friends


# Example: Get all friends of Alice with the relationship type "is_friend_of"
# friends_of_alice = find_friends("Alice", "IS_FRIEND_OF")
# print(friends_of_alice[0])


# Close the driver connection
driver.close()

uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"

# match(n) return n

driver = GraphDatabase.driver(uri, auth=(username))


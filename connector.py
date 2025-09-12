from pymongo import MongoClient
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

class MongoDBConnector:
    def __init__(self):
        self.connection_string = "mongodb+srv://maverick:maverick608@maverick.4njbt5n.mongodb.net/?retryWrites=true&w=majority&appName=maverick"
        self.client = None
        self.db = None
    
    def connect(self, database_name=None):
        """Connect to MongoDB Atlas"""
        try:
            self.client = MongoClient(self.connection_string)
            # Test the connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB Atlas!")
            
            if database_name:
                self.db = self.client[database_name]
                print(f"Connected to database: {database_name}")
            
            return True
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False
        except ServerSelectionTimeoutError as e:
            print(f"Server selection timeout: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
    def get_database(self, database_name):
        """Get a specific database"""
        if self.client:
            self.db = self.client[database_name]
            return self.db
        else:
            print("Not connected to MongoDB. Please connect first.")
            return None
    
    def get_collection(self, collection_name):
        """Get a specific collection from the current database"""
        if self.db is not None:
            return self.db[collection_name]
        else:
            print("No database selected. Please select a database first.")
            return None
    
    def list_databases(self):
        """List all databases"""
        if self.client:
            return self.client.list_database_names()
        else:
            print("Not connected to MongoDB. Please connect first.")
            return []
    
    def list_collections(self):
        """List all collections in the current database"""
        if self.db is not None:
            return self.db.list_collection_names()
        else:
            print("No database selected. Please select a database first.")
            return []
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            print("Connection closed.")
        else:
            print("No active connection to close.")

# Example usage
if __name__ == "__main__":
    # Create connector instance
    connector = MongoDBConnector()
    
    # Connect to MongoDB Atlas
    if connector.connect():
        # List available databases
        print("Available databases:", connector.list_databases())
        
        # Connect to 'maverick' database
        maverick_db = connector.get_database('maverick')
        
        # Create a collection with URL and Data fields
        collection = connector.get_collection('url_data')
        
        # Insert a sample document to establish the structure
        sample_document = {
            "URL": "https://example.com",
            "Data": "Sample data content"
        }
        
        # Insert the sample document
        result = collection.insert_one(sample_document)
        print(f"Created collection with document ID: {result.inserted_id}")
        
        # List collections in maverick database
        print("Collections in maverick database:", connector.list_collections())
        
        # Show the inserted document
        document = collection.find_one({"_id": result.inserted_id})
        print("Sample document:", document)
        
        # Close connection when done
        connector.close_connection()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from connector import MongoDBConnector

# Lifespan event handler (replaces deprecated on_event)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if connector.connect():
        connector.get_database('maverick')
        print("Connected to MongoDB and maverick database")
    else:
        print("Failed to connect to MongoDB")
    
    yield
    
    # Shutdown
    connector.close_connection()
    print("Database connection closed")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Maverick Data API", 
    description="API for managing URL and Data entries",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request/response
class DataEntry(BaseModel):
    Company: str
    URL: str
    Data: str

class DataEntryResponse(BaseModel):
    id: str
    Company: str
    URL: str
    Data: str
    message: str

class UpdateDataEntry(BaseModel):
    Company: Optional[str] = None
    URL: Optional[str] = None
    Data: Optional[str] = None

# Initialize MongoDB connector
connector = MongoDBConnector()

@app.get("/")
async def root():
    return {"message": "Maverick Data API is running"}

@app.post("/add_data", response_model=DataEntryResponse)
async def add_data(entry: DataEntry):
    """
    Add new Company, URL and Data entry to the database
    """
    try:
        collection = connector.get_collection('url_data')
        
        # Create document to insert
        document = {
            "Company": entry.Company,
            "URL": entry.URL,
            "Data": entry.Data
        }
        
        # Insert the document
        result = collection.insert_one(document)
        
        # Return response with inserted document ID
        return DataEntryResponse(
            id=str(result.inserted_id),
            Company=entry.Company,
            URL=entry.URL,
            Data=entry.Data,
            message="Data added successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding data: {str(e)}")

@app.get("/get_data")
async def get_all_data():
    """
    Retrieve all Company, URL and Data entries from the database
    """
    try:
        collection = connector.get_collection('url_data')
        
        # Retrieve all documents
        documents = list(collection.find())
        
        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        
        return {
            "count": len(documents),
            "data": documents
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

@app.get("/get_data/{entry_id}")
async def get_data_by_id(entry_id: str):
    """
    Retrieve a specific Company, URL and Data entry by ID
    """
    try:
        from bson import ObjectId
        collection = connector.get_collection('url_data')
        
        # Find document by ID
        document = collection.find_one({"_id": ObjectId(entry_id)})
        
        if document:
            document['_id'] = str(document['_id'])
            return document
        else:
            raise HTTPException(status_code=404, detail="Entry not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")

@app.put("/update_data/{entry_id}")
async def update_data(entry_id: str, entry: UpdateDataEntry):
    """
    Update an existing Company, URL and Data entry
    """
    try:
        from bson import ObjectId
        collection = connector.get_collection('url_data')
        
        # Build update document (only include non-None fields)
        update_doc = {}
        if entry.Company is not None:
            update_doc["Company"] = entry.Company
        if entry.URL is not None:
            update_doc["URL"] = entry.URL
        if entry.Data is not None:
            update_doc["Data"] = entry.Data
            
        if not update_doc:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Update the document
        result = collection.update_one(
            {"_id": ObjectId(entry_id)},
            {"$set": update_doc}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        # Return updated document
        updated_doc = collection.find_one({"_id": ObjectId(entry_id)})
        updated_doc['_id'] = str(updated_doc['_id'])
        
        return {
            "message": "Data updated successfully",
            "updated_data": updated_doc
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating data: {str(e)}")

@app.delete("/delete_data/{entry_id}")
async def delete_data(entry_id: str):
    """
    Delete a specific Company, URL and Data entry by ID
    """
    try:
        from bson import ObjectId
        collection = connector.get_collection('url_data')
        
        # Delete the document
        result = collection.delete_one({"_id": ObjectId(entry_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        return {"message": "Data deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting data: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
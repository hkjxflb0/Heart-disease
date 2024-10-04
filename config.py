from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://mirohitbh:1974%40Ram@fastapi.z4kib.mongodb.net/"  # Replace with your MongoDB URL

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.heart
prediction_collection = database.get_collection("heart")

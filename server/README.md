# 🧑‍💼 Employee Management API — FastAPI + MongoDB

A simple yet powerful RESTful API built with **FastAPI** and **MongoDB** for managing employee records — perfect for learning CRUD operations, validation, and database integration.

## 🚀 Features

- ✅ Add new employees  
- 📄 View all employee records  
- 🔍 Retrieve employee by ID  
- ✏️ Update employee details  
- ❌ Delete an employee record  
- 🔒 Input validation using **Pydantic**  
- ⚡ Fast performance with **FastAPI**

---

## 🛠️ Getting Started

### 1️⃣ Set Up Your MongoDB Cluster
- Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a free cluster
- Whitelist your IP and create a user
- Copy your connection string (e.g. `mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority`)

### 2️⃣ Configure Environment Variables
Create a `.env` file in your project root:

MONGO_URL=mongodb+srv://<username>:<password>@yourcluster.mongodb.net/?retryWrites=true&w=majority
### 3️⃣ Run the Application
Make sure you have FastAPI and Uvicorn installed:
pip install fastapi uvicorn python-dotenv pymongo
Then start the app:
uvicorn main:app --reload
Your API will be live at:
http://127.0.0.1:8000

Check out the automatic docs:
http://127.0.0.1:8000/docs (Swagger UI)
http://127.0.0.1:8000/redoc (ReDoc)

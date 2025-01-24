Retail T-Shirt Store QA

Overview
This application provides a seamless interface for querying a retail T-shirt store's inventory and sales database. Using advanced natural language processing techniques, the app translates user questions into SQL queries and retrieves the relevant data. The application is built using LangChain, OpenAI, Streamlit, and a MySQL database backend.

Features
1) Natural Language Interface: Users can ask questions in plain English.
2) Semantic Similarity Example Selector: Ensures high accuracy by leveraging example-based learning.
3) Dynamic SQL Query Generation: Translates user queries into SQL for execution.
4) Database Support: Supports MySQL with integration using SQLAlchemy.
5) Interactive Frontend: Built with Streamlit for a user-friendly interface.

Prerequisites
Python 3.9 or later
MySQL database
Streamlit
Python Libraries

Install the required libraries using pip:
pip install langchain openai chromadb streamlit pymysql python-dotenv

Environment Variables
Create a .env file in the project directory and include your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

Database Schema

Tables
t_shirts: Contains information about T-shirt inventory.
t_shirt_id: Unique identifier for each T-shirt.
brand: Brand name.
size: Size of the T-shirt.
color: Color of the T-shirt.
price: Price per T-shirt.
stock_quantity: Available stock.
discounts: Contains discount details.
t_shirt_id: Foreign key referencing the T-shirt.
pct_discount: Discount percentage.

Code Structure

Backend Logic:
chain(): Defines the LangChain-based query chain for interacting with the MySQL database.
Semantic similarity and prompt templates are used to fine-tune the model's responses.

Frontend Logic:
Uses Streamlit for user input and displaying the results.

Integration:
Combines the backend query chain with a user-friendly interface for seamless interaction.

Deployment
Run the App

Clone the repository:
git clone https://github.com/your-repo.git
Navigate to the project directory:
cd retail_tshirt_qa
Run the Streamlit app:
streamlit run app.py

Access the App
Oen a web browser and navigate to http://localhost:8501.

Example Questions
"How many Adidas T-shirts do I have in my store?"
"What is the total price of inventory for small-sized T-shirts?"
"How much revenue will be generated post-discount for Nike T-shirts?"

Troubleshooting
Common Issues

Database Connection Errors:
Ensure the database credentials (db_user, db_password, db_host, and db_name) are correct.
Verify that the MySQL server is running.

Missing Environment Variables:
Ensure the .env file contains your OpenAI API key.

Library Installation:
Run pip install -r requirements.txt to install all dependencies.

Future Enhancements
Support for additional databases like PostgreSQL.
Multi-language query support.
Advanced analytics and reporting capabilities.

Credits
Developed by [TasaduqRiyaz].

License

This project is licensed under the MIT License.


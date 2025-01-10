from langchain import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.utilities import SQLDatabase
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts import FewShotPromptTemplate,PromptTemplate
from dotenv import load_dotenv
load_dotenv()
import os

def chain():
    llm=OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'],temperature=0.2,model="gpt-3.5-turbo-instruct")
    db_user='root'
    db_password='Haziqbgsbu%40123' # here @ is encoded as %40
    db_host='127.0.0.1'
    db_name='atliq_tshirts'
    db=SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=3)
    db.table_info

    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    few_shots = [
        {
            "Question": "How many t-shirts we have left for nike in extra small size and black colour",
            "SQLQuery": "SELECT SUM(stock_quantity) AS total FROM t_shirts WHERE brand = 'Nike' AND size = 'XS' AND color = 'Black'",
            "SQLResult": "Result of the sql query",
            "Answer": '77'
        },
        {
            "Question": "How much is the price of the inventory for all the small sized t-shirts",
            "SQLQuery": "SELECT SUM(price * stock_quantity) AS total_price FROM t_shirts WHERE size = 'S'",
            "SQLResult": "Result of the sql query",
            "Answer": '29430'
        },
        {
            "Question": "if we have to sell all the levi t-shirts with discounts applied.How much revenue our store will generate post discounts",
            "SQLQuery": "SELECT SUM(a.total_revenue * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) FROM (SELECT SUM(stock_quantity * price) AS total_revenue, t_shirt_id FROM t_shirts WHERE brand = 'Levi' GROUP BY t_shirt_id) a LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id",
            "SQLResult": "Result of the sql query",
            "Answer": '22233.70'
        },
        {
            "Question": "how many white colored levi t-shirts do we have available",
            "SQLQuery": "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand='Levi' AND color='White'",
            "SQLResult": "Result of the sql query",
            "Answer": '89'
        },
        {
            "Question": "How much is the price of all white color levi t shirts?",
            "SQLQuery": "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand='Levi' AND color='White'",
            "SQLResult": "Result of the sql query",
            "Answer": '1454'
        },
        {
            "Question": "If we have to sell all the Nike’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?",
            "SQLQuery": "SELECT SUM(a.total_revenue * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) FROM (SELECT SUM(stock_quantity * price) AS total_revenue, t_shirt_id FROM t_shirts WHERE brand = 'Nike' GROUP BY t_shirt_id) a LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id",
            "SQLResult": "Result of the sql query",
            "Answer": '20780.1'
        },
    ]
    to_vectorize = [' '.join(example.values()) for example in few_shots]
    open_ai_embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    vector_store = Chroma.from_texts(to_vectorize, open_ai_embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vector_store,k=2)
    example_prompt = PromptTemplate(input_variables=["Question", "SQLQuery", "SQLResult", "Answer", ],
    template="\n Question:{Question}\nSQLQuery:{SQLQuery}\nSQLResult:{SQLResult}\nAnswer:{Answer}",
    )
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"]
    )
    new_chain = SQLDatabaseChain.from_llm(llm, db, prompt=few_shot_prompt,verbose=True)
    return new_chain
if __name__=='__main__':
    chain=chain()
    print(chain.run("How many Adidas t_shirts do I have in my store"))


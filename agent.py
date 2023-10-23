import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from sqlalchemy import Column, Integer, String, Table, Date, Float, insert, MetaData, create_engine
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
# from langchain.chains import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import Tool, load_tools, initialize_agent
import pandas as pd

def count_tokens(agent, query):
    with get_openai_callback() as cb:
        result = agent(query)
        print(f'Spent a total of {cb.total_tokens} tokens')

    return result

class CustomAgent:
    def __init__(self):
        # Load openai key
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        # OPENAI_API_KEY = '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'

        # instantiate LLM
        llm = OpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0
        )

        # Function to count the number of tokens our LLM has used
        metadata_obj = MetaData()

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv('data\cleaned_lab_df.csv')
        state_df = pd.read_csv('data/state_df.csv')
        bloom_time_df = pd.read_csv('data/bloom_time_df.csv')
        bloom_color_df = pd.read_csv('data/bloom_color_df.csv')

        # Create the database engine
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv('data\cleaned_lab_df.csv')
        state_df = pd.read_csv('data/state_df.csv')
        bloom_time_df = pd.read_csv('data/bloom_time_df.csv')
        bloom_color_df = pd.read_csv('data/bloom_color_df.csv')
        engine = create_engine('sqlite:///data/lab_db.db')

        # Insert the data from the DataFrame into the table
        with engine.connect() as conn:
            df.to_sql('plant_info', conn, if_exists='append', index=False)
            state_df.to_sql('plant_state', conn, if_exists='append', index=False)
            bloom_time_df.to_sql('plant_bloom_time', conn, if_exists='append', index=False)
            bloom_color_df.to_sql('plant_bloom_color', conn, if_exists='append', index=False)

        db = SQLDatabase(engine,sample_rows_in_table_info=6)
        sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, use_query_checker=True)

        plant_data_tool = Tool(
            name='Lab DB',
            func=sql_chain.run,
            description="Useful for when you need to answer questions about native plants. There are many states in the state column, so use Like when querying this column."
        )

        tools = load_tools([ "llm-math"], llm=llm)
        tools.append(plant_data_tool)

        self.zero_shot_agent = initialize_agent(
            agent="zero-shot-react-description", 
            tools=tools, 
            llm=llm,
            verbose=True,
            max_iterations=10,
        )

    def query(self,query_text):
        return count_tokens(self.zero_shot_agent,query_text)
import os
# from langchain.llms import OpenAI
from openai import OpenAI
import openai
from openai import AsyncOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from sqlalchemy import create_engine
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.sql_database import SQLDatabase
import json
# from langchain.chains import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents import Tool, load_tools, initialize_agent, AgentType, Tool
import pandas as pd
from langchain.chains import LLMMathChain
from langchain.sql_database import SQLDatabase
import openai
import time

# Load openai key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def count_tokens(agent, query):
    with get_openai_callback() as cb:
        result = agent(query)
        print(f"Spent a total of {cb.total_tokens} tokens")

    return result


class DatabaseAgent:
    def __init__(self):
        # instantiate LLM
        llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv("data/cleaned_lab_df.csv")
        state_df = pd.read_csv("data/state_df.csv")
        bloom_time_df = pd.read_csv("data/bloom_time_df.csv")
        bloom_color_df = pd.read_csv("data/bloom_color_df.csv")
        # Create the database engine
        engine = create_engine("sqlite:///data/lab_db.db")

        # Insert the data from the DataFrame into the table
        with engine.connect() as conn:
            df.to_sql("plant_info", conn, if_exists="append", index=False)
            state_df.to_sql("plant_state", conn, if_exists="append", index=False)
            bloom_time_df.to_sql(
                "plant_bloom_time", conn, if_exists="append", index=False
            )
            bloom_color_df.to_sql(
                "plant_bloom_color", conn, if_exists="append", index=False
            )

        db = SQLDatabase(engine, sample_rows_in_table_info=6)
        sql_chain = SQLDatabaseChain.from_llm(
            llm, db, verbose=True, use_query_checker=True
        )

        plant_data_tool = Tool(
            name="Lab DB",
            func=sql_chain.run,
            description="Useful for when you need to answer questions singlular native plants by species name. There are many states in the state column, so use Like and distinct when querying this column.",
        )

        tools = load_tools([], llm=llm)
        tools.append(plant_data_tool)

        self.zero_shot_agent = initialize_agent(
            agent="zero-shot-react-description",
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=10,
        )

    def query(self, query_text):
        return count_tokens(self.zero_shot_agent, query_text)


class SearchAgent:
    def __init__(self):
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        search = SerpAPIWrapper()
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful to ask questions. Try to break up the questions to make them more targeted.",
            )
        ]

        self.chat_agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
        )

    def query(self, query_text):
        return count_tokens(self.chat_agent, query_text)


class QuestionsAgent:
    def query(self, query_text,context):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that takes a user's question and breaks it down into a list of sub-questions given some context from the user.",
                },
                {
                    "role": "user",
                    "content": "Context:I live in NY and want to replace my backyard lawn with native flowers.Question:What types of plants should I grow in my backyard.",
                },
                {
                    "role": "assistant",
                    "content": '["What is the climate like in New York?", "Are there any specific native flower species that are known to thrive in New York?", "How much sunlight does your backyard receive during the day?", "What type of soil do you have in your backyard?", "What are your preferences for size, height, and blooming season of the flowers?", "Are there any specific wildlife or pollinators you would like to attract to your backyard?", "Are there any specific maintenance requirements or constraints you have for the plants?"]',
                },
                {"role": "user", "content": f"Context:{context} Question:{query_text}"},
            ],
        )
        return response

class ResponseAgent:
    def __init__(self) -> None:
        
        self.context = "Bot: Hello and welcome to Native plant garden app, where you can design a native garden for your outdoor spaces. This could be to replace an existing front or back lawn, as well as to enhance any outdoor area with vibrant, eco-friendly native plants. \nTo start, please give us your location, as well as information about the space you would like to transform, and anything else you think would be helpful.\n"
        self.questions = [] 
        self.goodQuestion = True
    def answer_question(self,input):
        self.context += input +'\n'
        if self.questions != []:
            self.question = self.questions.pop()
            print(self.question)
            # Try to answer it
            SearchAgent.query(self.question,self.context)
            # If the answer is bad and the question is good to ask then ask the user
            if(self.goodQuestion):
                self.questions = [] # only answers the first question
                return self.question
            else:
                return self.answer_question(input)
        if self.questions == []:
            # Get some questions and listify them
            print('test1')
            self.questions = json.loads(QuestionsAgent.query(self,input,self.context)['choices'][0]['message']['content'])
            print('test2')
            print(self.questions)
            return self.answer_question(input)
    def query_assistant(self,input):
                
        client = OpenAI()

        file_ids = ['file-vVW7Sh1T3PugpF9khPz0Pbx3','file-gTc3dLY0L2yGgZAdOgTkiLeL','file-ZVwmcQRa4UP6W6js6DVgjGJg','file-KLu8poyzhnCVFNBpPmOpgfoT']

        assistant_id = 'asst_UFpOwS7pizmlth0bMfUXoBx6'

        thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": input,
                "file_ids": file_ids
            }
        ]
        )
        print('>> Checking run status...')
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
            )
        while True:
            # Retrieve Run
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            print('run.status: ' + run.status)

            # Check if the run status is 'completed'
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(thread.id)
                if messages:
                    return messages.data[0].content[0].text.value
                break

            # Wait for 5 seconds before the next check
            print('>> Waiting 5 seconds before checking again...')
            time.sleep(5)

from openai import OpenAI
import time
client = OpenAI()

file_ids = ['file-vVW7Sh1T3PugpF9khPz0Pbx3','file-gTc3dLY0L2yGgZAdOgTkiLeL','file-ZVwmcQRa4UP6W6js6DVgjGJg','file-KLu8poyzhnCVFNBpPmOpgfoT']

# tools = [
#     {
#         "type": "code_interpreter"
#     }
# ]

# instructions = """You are a helpful assistant that helps people turn their outdoor spaces into native plant meadows. If you have any specific questions about flowers, use the data provided.

# The first file bloom_time_df.csv contains information about bloom time with columns "Accepted_SPNAME" and "BloomTime.L".

# The second file state_df.csv lists which states the plants are native to with columns "Accepted_SPNAME" and "State".

# The third file bloom_color_df.csv describes bloom colors with columns "Accepted_SPNAME" and "BloomColors".

# The fourth file cleaned_lab_df.csvappears to contain comprehensive information about the plants, including common names, sun tolerance, and other attributes with a variety of columns such as "Accepted_SPNAME", "CommonName.L"."""


# assistant = client.beta.assistants.create(
#     name="Meadow Chatbot",
#     instructions=instructions,
#     model="gpt-3.5-turbo-1106",
#     tools=tools,
#     file_ids= file_ids
# )

assistant_id = 'asst_UFpOwS7pizmlth0bMfUXoBx6'

msg = input('User:')
thread = client.beta.threads.create(
messages=[
    {
        "role": "user",
        "content": msg,
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
        thread_messages = client.beta.threads.messages.list(thread.id)
        print(thread_messages)
        if thread_messages:
            print(thread_messages)
        break

    # Wait for 5 seconds before the next check
    print('>> Waiting 5 seconds before checking again...')
    time.sleep(5)



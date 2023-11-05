# Notes

Figure out how to add custom descriptions for each agent

Bloom time for text to picture will be a big factor
GoBOtany and Inaturalist apps

<https://github.com/PandaWhoCodes/chatbot-frontend>
Render

Custom CSS:
<!-- vendor css & style files -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Josefin+Sans:300|Open+Sans:300|Oxygen|Material+Icons"
   rel="stylesheet">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">

Steps:

1) Initial Prompt : "Hello and welcome to Native plant garden app, where you can design a native garden for your outdoor spaces. This could be to replace an existing front or back lawn, as well as to enhance any outdoor area with vibrant, eco-friendly native plants. \n To start, please give us your location, as well as information about the space you would like to transform, and anything else you think would be helpful."


1) User - Question
2) Bot 1 - Take this question and some history and generate a list of things you would need to know before answering the question
   1) Take this list and try to answer some of the questions (Ask the user, Query database, ask an expert (serpAPI))
      <!-- 1) Ask the user -  -->
3) Bot 1 - Given this context(history,questions and answers) answer the following question
4) Bot 2 - Given this context(history) does this sufficiently answer the question? if not generate some questions to do so
   1) Repeat up to 2 times
5) GPT-AI - Response to question


Data structures:
AskUserFlag(Boolean)
Questions(list)
Answers(list)
AnsweredQuestions(dict)

Note: The plant database should be queried only for specific plant information.

https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/few_shot_examples


For later:
Querying local plant nurseries for native plants finding their catalog and comparing that to the curated native plant list

Presentation for lab December 12th:
What we have done, where we are, what where we are going - 
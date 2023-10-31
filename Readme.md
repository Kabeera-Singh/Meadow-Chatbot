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

possible second method

1) User - Question
2) Bot 1 - Take this question and some history and generate a list of things you would need to know before answering the question
   1) Take this list and try to answer some of the questions (Ask the user, Query database, ask an expert (serpAPI))

      1) Ask the user -
3) Bot 1 - Given this context(history,questions and answers) answer the following question
4) Bot 2 - Given this context(history) does this sufficiently answer the question? if not generate some questions to do so
   1) Repeat up to 2 times
5) App - Response to question
   1) Ask bot 2 to summarize the history with the new question/answer.

Data structures:
AskUserFlag(Boolean)
Questions(list)
Answeres(list)
AnsweredQuestions(dict)


https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/few_shot_examples

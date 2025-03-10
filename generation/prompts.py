"""
prompts.py
----------
Contient les PromptTemplates pour différentes étapes (RAG, grading, etc.).
"""

from langchain.prompts import PromptTemplate

# Exemple : Prompt pour un flux RAG
RAG_PROMPT = PromptTemplate(
    template="""
You are an assistant for question-answering tasks.
Use the following documents to answer the question. 
If you don't know the answer, just say that you don't know.

Use three sentences maximum and keep the answer concise:

Question: {question}
Documents: {documents}
Answer:
""",
    input_variables=["question", "documents"],
)

# Exemple : Prompt pour le retrieval grading
GRADING_PROMPT = PromptTemplate(
    template="""
You are a teacher grading quiz answers for relevance.  
Your task is to determine whether the student's provided FACT is relevant to the given QUESTION.

"Relevant" means the FACT directly helps answer, clarify, or is closely related to the QUESTION.

Output only valid JSON with a single key: "score" 
value should only be : 
- "yes" when relevant
- "no" when no relevant

Now grade the following:

QUESTION: {question}
FACT: {fact}
Output:
""",
    input_variables=["question", "fact"],
)


SEARCH_REWRITE_PROMPT = PromptTemplate(
    template="""
You are a helpful assistant. Your task is to generate a concise, well-structured query for a web search based on the user’s request. The goal is to capture the user’s intent accurately while removing ambiguity or unnecessary details.

You will be given a QUESTION

Process:

1. Read the user’s input carefully (QUESTION).
2. Rewrite the user’s input as a focused query.
3. Provide only the refined query as the final output, with no extra commentary or explanation."

User Prompt Example:
"User’s original question/request: {question}

Rewrite the above into a single search query that captures the main intent.

Output only valid JSON with a single key: "query_search" 
value should only be the text to search.
""",
    input_variables=["question"],
)
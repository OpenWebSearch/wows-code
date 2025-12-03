from outlines import prompt

# From https://github.com/castorini/umbrela/blob/main/src/umbrela/prompts/qrel_zeroshot_basic.txt
@prompt
def umbrella_zeroshot_basic(query: str, passage: str):
    """You are an expert judge of a content. Using your internal knowledge and simple commonsense reasoning, try to verify if the passage is relevance category to the query.
Here, "0" represent that the passage has nothing to do with the query, "1" represents that the passage seems related to the query but does not answer it, "2" represents that the passage has some answer for the query, but the answer may be a bit unclear, or hidden amongst extraneous information and "3" represents that the passage is dedicated to the query and contains the exact answer.

Provide explanation for the relevance and give your answer with from one of the categories 0, 1, 2 or 3 only. One of the categorical values if compulsory in answer.

Instructions: Think about the question. After explaining your reasoning, provide your answer in terms of 0, 1, 2 or 3 category. Only provide the relevance category on the last line. Do not provide any further details on the last line.

###

Query: {{query}}
Passage: {{passage}}

Explanation:
    """

# From https://github.com/castorini/umbrela/blob/main/src/umbrela/prompts/qrel_zeroshot_bing.txt
@prompt
def umbrella_zeroshot_bing(query: str, passage: str):
    """Given a query and a passage, you must provide a score on an integer scale of 0 to 3 with the following meanings:
0 = represent that the passage has nothing to do with the query, 
1 = represents that the passage seems related to the query but does not answer it, 
2 = represents that the passage has some answer for the query, but the answer may be a bit unclear, or hidden amongst extraneous information and 
3 = represents that the passage is dedicated to the query and contains the exact answer.

Important Instruction: Assign category 1 if the passage is somewhat related to the topic but not completely, category 2 if passage presents something very important related to the entire topic but also has some extra information and category 3 if the passage only and entirely refers to the topic. If none of the above satisfies give it category 0.

Query: {{query}}
Passage: {{passage}}

Split this problem into steps:
Consider the underlying intent of the search.
Measure how well the content matches a likely intent of the query (M).
Measure how trustworthy the passage is (T).
Consider the aspects above and the relative importance of each, and decide on a final score (O). Final score must be an integer value only.
Do not provide any code in result. Provide each score in the format of: ##final score: score without providing any reasoning.
    """


__all__ = sorted(list(['umbrella_zeroshot_basic', 'umbrella_zeroshot_bing']))


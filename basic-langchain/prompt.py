REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS_v1 = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question formatted according to format_instructions: {format_instructions}

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS_v2 = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following exact format:

Question: the input question you must answer
Thought: you should always think about what to do next
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original input question formatted EXACTLY as follows:
{format_instructions}

CRITICAL RULES (must follow):
- Do NOT output JSON in Thought, Action, or Observation.
- Only output JSON in the "Final Answer" line, matching {format_instructions}.
- Never write "Action: None". If no tool is needed, skip Action/Observation and go directly to:
  Thought: I now know the final answer
  Final Answer: <JSON>
- If you are close to the iteration limit, summarize and STILL produce the Final Answer JSON.


Begin!

Question: {input}
Thought:{agent_scratchpad}
"""


REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following exact format:

Question: the input question you must answer
Thought: you should always think about what to do next
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original input question formatted EXACTLY as follows:
{format_instructions}

CRITICAL RULES (must follow):
- Do NOT output JSON in Thought, Action, or Observation.
- Only output JSON in the "Final Answer" line, matching {format_instructions}.
- Never write "Action: None". If no tool is needed, skip Action/Observation and go directly to:
  Thought: I now know the final answer
  Final Answer: <JSON>
- If you are close to the iteration limit, summarize the findings and STILL produce the Final Answer as a single valid JSON object that matches the schema.

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

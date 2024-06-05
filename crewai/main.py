import os
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from indexclient import IndexChroma
from crewai import Agent, Task, Crew, Process

# Set environment variables
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"
os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Initialize vector store
vectorstore = IndexChroma(embedding_function=embeddings, network="mainnet")

# Index IDs
litProtocolDocsIndexId = "kjzl6kcym7w8yax70suh5xoet5rn5hzt7tyrep704xma8063n9mr9nx3qgowb8b"
indexNetworkDocsIndexId = "kjzl6kcym7w8y6rf31ljq3867je1l4vhw426g9e13dk2m3516z7yccz3x47t3l4"

# Create retriever tool
tool = create_retriever_tool(
    vectorstore.as_retriever(search_kwargs={'filter': {'indexId': {"$in": [litProtocolDocsIndexId, indexNetworkDocsIndexId]}}}),
    "index_retriever",
    "Searches and returns documents.",
)

# Senior Developer Agent
developer = Agent(
  role='Senior Developer',
  goal='Provide detailed technical explanations and code samples for {topic}',
  verbose=True,
  memory=True,
  backstory="An expert developer with extensive experience in building and integrating complex systems.",
  tools=[tool],
  allow_delegation=True
)

# Technical Writer Agent
technical_writer = Agent(
  role='Technical Writer',
  goal='Document the research and provide clear and concise technical documentation for {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "An experienced technical writer with a talent for making complex technical topics understandable and accessible."
  ),
  tools=[tool],
  allow_delegation=False
)

# Decomposition Task
decompose_task = Task(
  description=(
    "Decompose the main task of integrating {topic} into smaller, manageable sub-tasks. "
    "Each sub-task should have a clear objective and expected output."
  ),
  expected_output='A list of detailed sub-tasks',
  tools=[tool],
  agent=developer,
)

# Research Task
research_task = Task(
  description=(
    "Conduct in-depth research on {topic}. "
    "Provide detailed technical explanations and code samples where applicable."
  ),
  expected_output='A detailed technical report including code samples',
  tools=[tool],
  agent=developer,
)



# Forming the Crew with enhanced configurations
crew = Crew(
  agents=[developer, technical_writer],
  tasks=[decompose_task, research_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

# Kickoff the crew process with the specified topic
result = crew.kickoff(inputs={'topic': 'How to integrate Ceramic & Lit Protocol'})
print(result)

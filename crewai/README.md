# Index Network & CrewAI Integration

## Bringing a composable vector database with autonomous agents together

Integrating various protocols in the decentralized world of Web3 can be a complex and time-consuming task. This case study demonstrates how autonomous agents can streamline and automate the integration process over composable indexes, which eliminate data fragmentation, enhance synthesis capabilities, and enable seamless data sharing. In this example, we use CrewAI as an agent framework and Ceramic and Lit Protocol software documentation indexes as practical examples.

### What is CrewAI?

CrewAI enables AI agents to work together by defining specific roles, shared goals, and custom tools. It enhances interactions through structured processes and task delegation.

## Demonstrated Autonomous Agents

In this work, we use two types of agents:

1.  **Senior Developer Agent**: Provides detailed technical explanations and code samples for integrations.
2.  **Technical Writer Agent**: Documents the integration process, ensuring clarity and accessibility of technical instructions.

These agents work together to conduct comprehensive research, develop technical guides, and produce high-quality documentation, simplifying the integration process for developers.

## Setup

### Environment Configuration

First, set up the environment variables and initialize the necessary embeddings and vector store for document retrieval.

```python
import os
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from indexclient import IndexChroma
from crewai import Agent, Task, Crew, Process

os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"
os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = IndexChroma(embedding_function=embeddings, network="mainnet")
```

### Document Retrieval

Create a Index Network as a retriever tool to search and return relevant documents for the integration of decentralized protocols.

```python
tool = create_retriever_tool(
    vectorstore.as_retriever(search_kwargs={'filter': {'indexId': {"$in": [litProtocolDocsIndexId, indexNetworkDocsIndexId]}}}),
    "index_retriever",
    "Searches and returns documents.",
)
```

### Agent Configuration

Define two agents with specific roles and goals.

```python
developer = Agent(
  role='Senior Developer',
  goal='Provide detailed technical explanations and code samples for {topic}',
  verbose=True,
  memory=True,
  backstory="An expert developer with extensive experience in building and integrating complex systems.",
  tools=[tool],
  allow_delegation=True
)

technical_writer = Agent(
  role='Technical Writer',
  goal='Document the research and provide clear and concise technical documentation for {topic}',
  verbose=True,
  memory=True,
  backstory="An experienced technical writer with a talent for making complex technical topics understandable and accessible.",
  tools=[tool],
  allow_delegation=False
)
```

### Task Creation

Create tasks for the agents to conduct research and document the integration process.

```python
research_task = Task(
  description=(
    "Conduct in-depth research on {topic}. "
    "Provide detailed technical explanations and code samples where applicable."
  ),
  expected_output='A detailed technical report including code samples',
  tools=[tool],
  agent=developer,
)

documentation_task = Task(
  description=(
    "Create comprehensive documentation on integrating {topic}. "
    "The documentation should include clear explanations, code samples, and step-by-step instructions."
  ),
  expected_output='A well-structured technical documentation in markdown format',
  tools=[tool],
  agent=technical_writer,
  async_execution=False,
  output_file='integration-guide.md'
)

```

### Crew Formation and Process Initiation

Form a crew with the defined agents and tasks, and initiate the process with the specified topic.

```python
crew = Crew(
  agents=[developer, technical_writer],
  tasks=[research_task, documentation_task],
  process=Process.sequential,
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)
result = crew.kickoff(inputs={'topic': 'How to integrate Ceramic & Lit Protocol'})
print(result)
```

## Result

The collaborative effort of the Senior Developer and Technical Writer agents results in a detailed integration guide. This guide provides step-by-step instructions, detailed technical explanations, and code samples for integrating decentralized protocols.

## Relevant Links

- Website: https://index.network
- Documentation: https://docs.index.network
- Github: https://github.com/indexnetwork/index
- Discord: https://discord.gg/XkQw8gDVw4
- X: https://x.com/indexnetwork_

If you are interested in decentralized information discovery and what we are building at Index Network, we would love to hear from you.

Please reach out to us at [hello@index.network](mailto:hello@index.network)

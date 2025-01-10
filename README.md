# Scientific AI Agents built with autogen

A framework for building scientific AI agents that can collaborate and solve complex research problems.

## Features

- Multi-agent collaboration system
- Scientific research workflow automation
- Extensible agent architecture

## Prerequisites

- Python 3.8+
- AutoGen library
- OpenAI API key
- Ollama
- Ollama run gemma2:2b
- llamaindex

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

1. Set up your environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

2. Run the basic example:
```bash
python main.py
```

## Agent Roles and Workflow

### Agents

1. **Planner Agent**
   - Breaks down research queries into sub-tasks
   - Coordinates research workflow
   - Ensures comprehensive topic coverage
   - Maintains scientific rigor

2. **Scientist Agent**
   - Searches and analyzes scientific papers
   - Uses arXiv and Google Scholar APIs
   - Verifies paper citations
   - Provides evidence-based analysis

3. **Ontologist Agent**
   - Maps relationships between concepts
   - Creates knowledge representations
   - Maintains terminology consistency
   - Identifies key terms and definitions

4. **Critic Agent**
   - Evaluates research proposals
   - Identifies methodological issues
   - Assesses research novelty
   - Suggests improvements

5. **Assistant Agent**
   - Summarizes agent discussions
   - Provides final answers
   - Includes relevant citations
   - Highlights research limitations

### Workflow

1. **Query Processing**
   - User submits research question
   - Planner breaks down the query
   - Research plan is formulated

2. **Literature Search**
   - Scientist searches paper databases
   - Verifies paper authenticity
   - Analyzes research findings

3. **Knowledge Mapping**
   - Ontologist creates concept maps
   - Links related research areas
   - Standardizes terminology

4. **Critical Review**
   - Critic evaluates findings
   - Checks methodology
   - Identifies gaps

5. **Final Synthesis**
   - Assistant summarizes findings
   - Compiles comprehensive answer
   - Cites verified sources
   - Suggests future research

## Sample Output

- Question: 

```
What are attention mechanisms in LLMs?
```

- Answer:

```
assistant (to chat_manager):

Based on the discussion between agents, here is a summary:

The Scientist found three key papers that discuss the concept of attention mechanisms: "Attention is All you Need" by Vaswani et al. (ARXIV, 1706.03762), "Neural Machine Translation by Jointly Learning to Align and Translate" by Bahdanau et al. (ARXIV, 1409.0473), and "Effective Approaches to Attention-based Neural Machine Translation" by Luong et al. (ARXIV, 1508.04025). 

These papers explain that attention mechanisms allow models to focus on different parts of the input sequence when producing an output. This improves the model's ability to handle long sequences and complex relationships.

As for the application of attention mechanisms in Language Learning Models (LLMs), different types of attention mechanisms used in LLMs, the benefits and drawbacks of using attention mechanisms in LLMs, and the future prospects of attention mechanisms in LLMs, further research is required.

In conclusion, attention mechanisms in LLMs are techniques that allow models to focus on different parts of the input sequence when producing an output, thereby improving the model's ability to handle long sequences and complex relationships. Further research is needed to fully understand their application, types, benefits, drawbacks, and future prospects in LLMs.
```
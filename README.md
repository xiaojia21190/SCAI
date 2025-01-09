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


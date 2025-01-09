# Scientific AI Agents built with autogen

A framework for building scientific AI agents that can collaborate and solve complex research problems.

## Features

- Multi-agent collaboration system
- Scientific research workflow automation
- Cursor composer pattern for response management
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
python examples/basic_research.py
```

## Usage

1. Create your agent configuration:
```python
from scientific_agents import ResearchAgent, AnalysisAgent

researcher = ResearchAgent()
analyst = AnalysisAgent()
```

2. Define your research query:
```python
query = "Investigate the effects of temperature on protein folding"
```

3. Run the agent collaboration:
```python
results = researcher.collaborate_with(analyst, query)
```

## Advanced Configuration

See `config/` directory for detailed configuration options and examples.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
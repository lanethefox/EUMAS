# Project EUMAS: Unified Memory and Archetype System

## Project Overview
EUMAS is an advanced conversational AI framework designed to create deeply personalized, contextually rich interactions using multiple archetypal perspectives.

## Setup and Installation

### Prerequisites
- Python 3.11+
- pip
- (Optional) Virtual Environment recommended

### Installation Steps
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

## Key Dependencies
- OpenAI GPT-4O
- Milvus Vector Database
- Transformers
- Sentence Transformers

## Development
- Use `pytest` for testing
- Use `black` for code formatting
- Use `mypy` for type checking
- Use `ruff` for linting

## Security Notes
- Never commit API keys or sensitive information to version control
- Use environment variables for configuration

## Licensing
[Add your licensing information here]

## Contributing
[Add contribution guidelines]

# Web Search Assistant

## Overview
The Web Search Assistant is a Python application designed to enhance web search capabilities by utilizing various agents to analyze queries, retrieve information, and generate concise responses.

## Project Structure
- **src/**: Contains the main application code.
  - **agents/**: Implements different agents for keyword analysis, web searching, scraping, and response generation.
  - **templates/**: Holds prompt templates for guiding language models.
  - **utils/**: Provides utility functions for web scraping and JSON handling.
  - **config/**: Contains configuration settings.
  - **main.py**: The entry point for the application.
- **tests/**: Contains unit tests for agents and utility functions.
- **requirements.txt**: Lists project dependencies.
- **.env**: Contains environment variables.

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd web-search-assistant
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables in the `.env` file.

## Usage
Run the application using:
```
python src/main.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.
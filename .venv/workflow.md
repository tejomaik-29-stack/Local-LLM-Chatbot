flowchart TD
    A[User enters a question] --> B[Streamlit Frontend]
    B --> C[Python Backend]
    C --> D[Ollama API]
    D --> E[Llama 3.2 1B Model]
    E --> F[Generates Answer]
    F --> G[Displays Answer to User]S
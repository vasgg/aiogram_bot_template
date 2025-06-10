# Bot Template

A modern aiogram Telegram bot template with rapid project setup powered by [uv](https://github.com/astral-sh/uv).

## 📦 Installation

**Requirements:** [uv](https://github.com/astral-sh/uv)

- Clone the repository and navigate to your project folder:

    ```bash
    git clone https://github.com/vasgg/aiogram_bot_template.git
    cd aiogram_bot_template
    ```

- Create and activate a virtual environment:

    ```bash
    uv sync
    ```

- Install all dependencies from `pyproject.toml`:

    ```bash
    uv pip install -Ue .
    ```

- Create your `.env` file (see example in `.env.example`) and set all required environment variables.

## 🚀 Running the Bot

- After installation and environment setup, simply run::

   ```bash
   bot-run
   ```

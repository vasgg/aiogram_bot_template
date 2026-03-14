# Bot Template

A modern Telegram bot template with rapid project setup powered by [uv](https://github.com/astral-sh/uv) and [aiogram](https://github.com/aiogram/aiogram).

## 🧩 Using this repository as a project template
- On GitHub, click **"Use this template"** (green button) to create your own repository based on this template.

- Update `pyproject.toml`:
    - Change the `name`, `description`, `authors`, and any other relevant fields.

- Update `.env` as needed for your project.

- Follow the installation and usage steps below.

That's it — you're ready to build your own aiogram bot!

## 📦 Installation

**Requirements:** [uv](https://github.com/astral-sh/uv)

- Set up the development environment and install runtime + dev dependencies:

    ```bash
    make install-dev
    ```

- If you only need runtime dependencies, use:

    ```bash
    make install
    ```

- Start local infrastructure for development:

    ```bash
    make db-up
    ```

- Create your `.env` file from `.env.example`. The example is prefilled for local Postgres on `127.0.0.1:5444` and Redis at `redis://127.0.0.1:6379/0`.

## 🛠 Common Commands

```bash
make run
make check
make db-up
make db-down
make migrate
make revision MESSAGE=add_users_table
```

## 🚀 Running the Bot

- After installation and environment setup, simply run:

   ```bash
   make run
   ```

# Qwen Code Project Configuration

## Project Identity
name: Sistema de Coleta Financeira
type: python-application
language: Python 3.12
framework: Streamlit, Discord.py, PostgreSQL
package_manager: pip

## Key Directories
src: src/
tests: tests/
docs: docs/
scripts: scripts/
data: data/
logs: logs/

## Commands
install: pip install -r requirements.txt
test: pytest tests/
lint: ruff check src/
build: docker compose build
start: docker compose up
dev_bot: python -m src.bot_discord
dev_web: streamlit run src/interface/app.py
dev_collect: python -m src.pipeline

## Conventions
# - Portuguese (Brazil) comments and strings where they exist
# - Coinbase API wrapper pattern for all exchange integrations
# - Database access through db_manager.py only
# - Docker Compose for deployment
# - Environment variables via .env file
# - Logging through src/utils/logger.py

## File Patterns to Watch
python: "**/*.py"
config: "**/*.yml, **/*.yaml, **/*.env"
docker: "Dockerfile, docker-compose.yml, .dockerignore"
docs: "**/*.md"

## MCP Integration Points
# - postgres: Query collected crypto data
# - docker: Manage containers (status, logs, restart)
# - github: PR reviews, issues, actions
# - filesystem: Navigate project structure

## Agent Quick Reference
# Use Explore agent for: finding files, searching code, understanding architecture
# Use general-purpose agent for: implementing features, refactoring, writing tests
# Always specify thoroughness: quick / medium / very thorough

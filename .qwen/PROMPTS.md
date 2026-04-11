# Workflow Prompts — Sistema de Coleta Financeira

Copy and paste these prompts directly into Qwen Chat.

---

## Exploration & Understanding

### Understand a specific component
```
Explore the codebase and explain how [component] works. Be very thorough.
Examples:
- "Explore the codebase and explain how the alert system works. Be very thorough."
- "Explore the codebase and find all Discord command handlers. Be medium."
```

### Find specific code patterns
```
Search for [pattern] across all Python files.
Examples:
- "Search for all database queries across all Python files"
- "Search for all uses of Coinbase API"
- "Search for error handling patterns"
```

### Map dependencies
```
Map all dependencies between [module A] and [module B]. Show the import chain.
Example: "Map all dependencies between pipeline.py and the collectors"
```

---

## Implementation Tasks

### Add a new cryptocurrency
```
I want to add [SYMBOL] to the monitoring system. Read src/pipeline.py and add it to ATIVOS_DISPONIVEIS. Then verify the dynamic collector handles it.
```

### Write unit tests
```
Write comprehensive unit tests for [module]. Mock external APIs, test edge cases, and follow Python testing best practices. Save to tests/test_[module].py.
Examples:
- "Write comprehensive unit tests for the collectors"
- "Write comprehensive unit tests for the database manager"
- "Write comprehensive unit tests for the alert system"
```

### Implement a new feature
```
Implement [feature]. Read the relevant files first, plan the changes, then implement. Add tests.
Examples:
- "Implement a REST API endpoint for price queries"
- "Implement per-user Discord alert thresholds"
- "Implement Binance as a secondary exchange source"
- "Implement price prediction using moving averages"
```

### Refactor code
```
Refactor [module] to improve [aspect]. Read the current code first, then make changes while preserving functionality.
Examples:
- "Refactor the Discord bot to use cog classes instead of global functions"
- "Refactor the alert system to support configurable thresholds per asset"
- "Refactor database queries to use async/await"
```

---

## Code Quality & Review

### Review changes
```
/review [file_path]
Or after making changes: "Review the changes I just made to [file]"
```

### Add type hints
```
Add Python type hints to [module]. Read the file first, then add typing to all functions and methods.
```

### Improve error handling
```
Review error handling in [module]. Add proper try/except blocks, logging, and user-friendly error messages where missing.
```

### Security audit
```
Audit [module] for security issues: SQL injection, exposed secrets, input validation, etc.
```

---

## Docker & Deployment

### Debug Docker issues
```
Check Docker status and logs. Identify any services that aren't running properly and suggest fixes.
```

### Optimize Docker
```
Review the Dockerfile and docker-compose.yml. Suggest and implement optimizations for build time and image size.
```

### Set up CI/CD
```
Set up GitHub Actions workflow with: pytest, Docker build check, and linting. Create .github/workflows/ci.yml
```

---

## Database & Data

### Query data (requires postgres MCP)
```
Query the database to show me:
- Last 10 BTC prices collected
- Assets with highest 24h variation
- Collection frequency statistics
```

### Create a migration
```
Create a database migration script to [change]. Read db_manager.py first to understand the schema.
```

### Export/import data
```
Create a script to export collected price data to [format: CSV/JSON/Excel] with proper timestamps and formatting.
```

---

## Documentation

### Update README
```
Update README.md to reflect the current state of the project. Include new features, commands, and setup instructions.
```

### Write docstrings
```
Add comprehensive docstrings to all functions in [module]. Include parameters, return types, and examples.
```

### Create architecture diagram
```
Create a text-based architecture diagram showing how all components interact. Save to docs/architecture.md
```

---

## Automation & Scheduling

### Browser Testing (Playwright MCP)
```
Use Playwright to test the Streamlit web interface.
Examples:
- "Open localhost:8501 and verify all 6 pages load correctly"
- "Navigate to the Dashboard page and take a screenshot of the charts"
- "Test the manual collection button on the Coleta page"
- "Verify the home page shows correct system status metrics"
- "Test the alert configuration page and check if Discord webhook field works"
```

### Set up recurring tasks
```
/loop 30m check if collector container is running and report status
```

### Create a monitoring script
```
Create a script that monitors [metric] and sends alerts to Discord when thresholds are exceeded.
Examples:
- "Create a script that monitors collection frequency and alerts if gaps > 10 minutes"
- "Create a script that monitors database size and alerts if it grows too large"
```

---

## Tips for Better Results

1. **Always provide context**: "In src/bot_discord.py, the !comparar command..."
2. **Specify output format**: "Save to tests/test_collectors.py"
3. **Ask for explanations**: "Explain why you made this change"
4. **Iterate**: Start small, review, then expand
5. **Use agents for complexity**: For tasks requiring 3+ steps, ask Qwen to use the agent tool
6. **Verify with commands**: "Run pytest to verify the changes"

---

## Anti-Patterns to Avoid

❌ "Fix the bot" → ✅ "Fix the !top command embed formatting in src/bot_discord.py"
❌ "Make it better" → ✅ "Add error handling to all database queries in db_manager.py"
❌ "Add tests" → ✅ "Write unit tests for src/alertas.py covering variation and limit alerts"
❌ "Optimize Docker" → ✅ "Reduce Docker image size by using multi-stage builds"

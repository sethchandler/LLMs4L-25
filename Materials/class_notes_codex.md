# Codex Prompt Playbook: Reproducing the NextGen Outline Tool

Use these prompts to guide Codex (the coding assistant) from an empty directory to the completed project. Each prompt assumes Codex sees the project root and has shell access. Adjust the directory names if your environment uses something different.

> **Tip**: After each prompt, wait for Codex to finish running commands or creating files before issuing the next one. If Codex asks for clarification, answer before proceeding.

---

## Stage 1 — Workspace Setup

### Prompt 1
```
Create a new folder called NextGen in ~/dev (create ~/dev if needed) and cd into it. Initialize a git repository here.
```

Expected actions:
- `mkdir -p ~/dev/NextGen`
- `cd ~/dev/NextGen`
- `git init`

### Prompt 2
```
Initialize a Poetry project named nextgen-outline targeting Python 3.11, and add httpx, rich, and python-dotenv as dependencies.
```

Expected outcome: `pyproject.toml` and `poetry.lock` with the dependencies declared.

---

## Stage 2 — Resources and Base Script

### Prompt 3
```
Create a Resources directory. Inside it, add a file NextGen_outline containing the full bar exam outline text (paste the markdown). Also add NextGen Segment.md containing the prompt template. Finally, generate a README with setup instructions.
```

Codex should create:
- `Resources/NextGen_outline`
- `Resources/NextGen Segment.md`
- `README.md` (initial stub)

### Prompt 4
```
Write process_outline.py that reads Resources/NextGen_outline, splits on ## and ### headings, assigns sequential id numbers starting at 1, and writes Resources/NextGen_outline.json with fields id, section, subsection, outline_source, and content (both populated with the outline text). Run the script.
```

Check `Resources/NextGen_outline.json` afterward to ensure IDs exist.

---

## Stage 3 — CLI Tool

### Prompt 5
```
Create a package nextgen_outline with __init__.py and cli.py. The CLI should parse arguments (input, prompt-file, output, model with default google/gemini-2.5-flash-lite, system-prompt, entries, max-retries, retry-wait, temperature, max-tokens, concurrency, referer, title, api-key). It must load .env automatically, read the outline JSON, ensure outline_source exists (defaulting from content), and asynchronously call the OpenRouter API with retries, saving incremental results to the output file. Use rich for progress output, httpx for requests, and an asyncio.Lock to guard writes.
```

Confirm the script is complete and references the correct headers (`HTTP-Referer`, `X-Title`).

### Prompt 6
```
Update pyproject.toml to register a console script called nextgen-augment pointing to nextgen_outline.cli:main. Ensure the dependencies section still lists httpx, rich, and python-dotenv.
```

Run `poetry install` if Codex doesn’t do it automatically.

---

## Stage 4 — Configuration and Documentation

### Prompt 7
```
Create a .env file with placeholders for OPENROUTER_API_KEY and optional OPENROUTER_HTTP_REFERER and OPENROUTER_TITLE. Update README.md so the usage example shows the default model google/gemini-2.5-flash-lite, mentions the referer/title flags, and includes a CLI options table with defaults.
```

### Prompt 8
```
Add class_notes.md containing a detailed, beginner-friendly walkthrough for the live classroom coding session, covering terminology, setup, commands, and troubleshooting tips.
```

### Prompt 9
```
Add class_notes_codex.md summarizing these Codex prompts so we can recreate the repository from scratch.
```

---

## Stage 5 — Finalization

### Prompt 10
```
Run poetry run python process_outline.py and poetry run nextgen-augment --help to confirm everything works. Then create a .gitignore that ignores .env, __pycache__/ directories, *.pyc files, and .DS_Store.
```

### Prompt 11
```
Stage all files and create an initial git commit with the message "Initial outline tooling".
```

---

## Optional Follow-Up Prompts

- Test a small augmentation run:
  ```
  Run poetry run nextgen-augment --entries 1-2 --model google/gemini-2.5-flash-lite --referer https://example.com
  ```
- Regenerate the outline if resources change:
  ```
  Re-run process_outline.py after updating the outline source file.
  ```
- Show how to adjust models:
  ```
  Update README.md with instructions for using --model to select alternate OpenRouter models.
  ```

By following these prompts in order, Codex should recreate the repository exactly, minimizing mistakes during the live demonstration.

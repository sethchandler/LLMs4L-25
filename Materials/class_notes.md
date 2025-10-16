# Live Coding Plan: NextGen Outline Augmenter

This guide is for running a classroom demonstration that builds the **NextGen outline augmenter** from scratch. It assumes the instructor and students have almost no programming background. Every step is spelled out; jargon (specialized vocabulary) is defined the first time it appears.

---

## 1. Vocabulary Cheat Sheet

- **Terminal / Command Line**: A text-only window where you type commands and press Enter to make the computer do things (create folders, run programs, etc.). On a Mac this is the *Terminal* app.
- **Command**: A line of text you type into the terminal. Example: `mkdir NextGen`.
- **Shell**: The program that reads commands in the terminal. macOS uses `zsh` by default.
- **Path**: The address of a file or folder on your computer, like `/Users/Seth/dev/NextGen`.
- **Repository (repo)**: A project tracked by the version-control tool *Git*. It remembers changes to files.
- **Git**: A tool that records file history and lets you undo or share work.
- **Commit**: A saved snapshot in Git.
- **Python**: A programming language we use to write scripts.
- **Poetry**: A helper tool that manages Python project settings and libraries (extra pieces of code).
- **Virtual environment**: A safe area created by Poetry where our project-specific Python libraries live.
- **Environment variable**: A named value the operating system stores for programs. We will use one to store the OpenRouter API key. API key = secret password for web service.
- **JSON (JavaScript Object Notation)**: A plain-text format for data. Looks like nested braces `{}` and lists `[]`.

Encourage students to refer back to this list whenever they see an unfamiliar term.

---

## 2. Prerequisites (Set Up Before Class)

1. **macOS tools installed**
   - Python 3.11 or later (`python3 --version` should show 3.11+).
   - [Poetry](https://python-poetry.org/docs/#installation). Check with `poetry --version`.
   - Git (`git --version`).
2. **OpenRouter account** with an API key. Copy the key somewhere safe.
3. **Folders prepared**
   - Create a parent folder where student projects will live (example: `~/dev`).
4. **Terminal practice**
   - Open Terminal and run a few sample commands (`pwd`, `ls`, `mkdir`). Make sure you are comfortable describing what they do.

Tip: If any tool is missing, install it *before* class so you don’t burn demonstration time troubleshooting installers.

---

## 3. High-Level Plan

Students will see the following stages:

1. Create a project folder and move into it.
2. Initialize Git and Poetry.
3. Save the outline resources.
4. Build the `process_outline.py` script to generate JSON with IDs.
5. Build the `nextgen_outline` package and command-line tool to call OpenRouter.
6. Create configuration files (`pyproject.toml`, `.env`, `README.md`, `class_notes.md`).
7. Test the tool in “dry run” mode (no real API call).
8. Run a live augmentation on a small entry range.
9. Make a Git commit.

Breaks are built in for questions—expect to pause after each major step.

---

## 4. Step-by-Step Demonstration Script

### Step 0 — Open a Clean Terminal Session

```bash
cd ~
pwd
```

Explain `pwd` (“print working directory”) so students know where they are.

### Step 1 — Create the Project Directory

```bash
mkdir -p ~/dev/NextGen
cd ~/dev/NextGen
pwd
```

Talk through what `mkdir -p` does (make directory, no error if it already exists) and why we change directories with `cd`.

### Step 2 — Initialize Git

```bash
git init
git branch --show-current
```

Mention that `master` is the default branch name. Stress that Git is optional for the tool, but essential for tracking mistakes.

### Step 3 — Initialize Poetry

```bash
poetry init --no-interaction \
  --name "nextgen-outline" \
  --dependency httpx \
  --dependency rich \
  --dependency python-dotenv
```

Explain:
- `poetry init` creates the project configuration file `pyproject.toml`.
- `httpx` is how we make web requests.
- `rich` gives progress bars.
- `python-dotenv` loads the secret API key from a `.env` file.

Verify the new files:

```bash
ls
cat pyproject.toml
```

### Step 4 — Create Resource Files

1. `Resources/NextGen_outline` (source outline).
2. `Resources/NextGen Segment.md` (prompt template).

Commands:

```bash
mkdir Resources
```

Open a text editor (VS Code, TextEdit, or `nano`) to paste the outline and prompt. Stress good file naming: no spaces except where required.

### Step 5 — Build `process_outline.py`

Explain the goal: convert the Markdown outline into JSON with sequential IDs.

Create the file (use editor or cat-heredoc). Example with `cat` so students see direct terminal editing:

```bash
cat <<'PY' > process_outline.py
import json
from pathlib import Path


def parse_outline(outline_text: str):
    entries = []
    current_section = None
    current_entry = None

    for raw_line in outline_text.splitlines():
        line = raw_line.rstrip()

        if line.startswith("## "):
            current_section = line[3:].strip()
            current_entry = None
            continue

        if line.startswith("### "):
            subsection = line[4:].strip()
            current_entry = {
                "section": current_section,
                "subsection": subsection,
                "content": [],
            }
            entries.append(current_entry)
            continue

        if current_section and current_entry:
            stripped = line.strip()
            if not stripped or set(stripped) == {"-"}:
                continue
            current_entry["content"].append(stripped)

    normalized = []
    for idx, entry in enumerate(entries, start=1):
        content = "\n".join(entry["content"])
        normalized.append(
            {
                "id": idx,
                "section": entry["section"],
                "subsection": entry["subsection"],
                "outline_source": content,
                "content": content,
            }
        )

    return {"entries": normalized}


def main():
    project_root = Path(__file__).parent
    outline_path = project_root / "Resources" / "NextGen_outline"
    output_path = project_root / "Resources" / "NextGen_outline.json"

    outline_text = outline_path.read_text(encoding="utf-8")
    outline_data = parse_outline(outline_text)

    output_path.write_text(json.dumps(outline_data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
PY
```

Run the script:

```bash
python3 process_outline.py
head Resources/NextGen_outline.json
```

Call out that each entry has an `id`, `section`, `subsection`, `outline_source`, and `content`.

### Step 6 — Create the CLI Package

1. Make package folder and initializer:

```bash
mkdir nextgen_outline
echo '"""NextGen outline tools package."""' > nextgen_outline/__init__.py
```

2. Create `nextgen_outline/cli.py` with the full script (already in repo). For class, paste the prepared version to avoid typos.

Key code concepts to point out:
- We parse command-line options with `argparse`.
- We use `asyncio` and `httpx` to send requests.
- For each entry, we build a prompt and call the OpenRouter API.
- We write partial results right away so progress is saved.

After saving the file, show students how to read parts using `sed -n '1,20p nextgen_outline/cli.py'`.

### Step 7 — Update `pyproject.toml` Script Section

Add the console script entry so Poetry exposes `nextgen-augment`.

Show the `[tool.poetry.scripts]` section:

```toml
[tool.poetry.scripts]
nextgen-augment = "nextgen_outline.cli:main"
```

### Step 8 — Create `.env` for Secrets

```bash
cat <<'EOF' > .env
OPENROUTER_API_KEY=sk-your-key-here
OPENROUTER_HTTP_REFERER=https://your-demo-site.example
# OPENROUTER_TITLE=Optional custom title
EOF
```

Explain:
- `.env` must never be shared publicly.
- `python-dotenv` will load it automatically when the CLI starts.

### Step 9 — Install Dependencies

```bash
poetry install
```

If errors appear, read them aloud and walk through the fix (e.g., “Python version incompatible” → update Python or adjust Poetry’s config).

### Step 10 — Test Commands (No Network Yet)

```bash
poetry run python process_outline.py        # should finish instantly
poetry run nextgen-augment --help          # confirm the CLI options
```

Stress that `poetry run` ensures we use the virtual environment Poetry created.

### Step 11 — Dry Run with Real Entries

1. Start small to avoid hitting rate limits or quota:

```bash
poetry run nextgen-augment --entries 1-2 --model google/gemini-2.5-flash-lite
```

2. Explain the output:
   - The script shows a progress bar.
   - Resume is possible because `Resources/NextGen_outline_augmented.json` updates after each success.
3. Show students the new JSON fields (`content` now holds the model’s answer; `outline_source` keeps the original text).

### Step 12 — Commit the Work

```bash
echo ".env" >> .gitignore
git status
git add .
git commit -m "Initial outline tooling"
```

Explain what `git status` means:
- Green files staged for commit.
- Red files not staged.
- `.env` should show as “ignored.”

### Step 13 — Stretch Goal (Optional)

- Demonstrate re-running the augmenter for a specific range: `--entries 13-14`.
- Show how to change the model with `--model openai/gpt-4o-mini` (optional if the default fails).
- Emphasize how to troubleshoot a 400 error (check API key, referer, model name).

---

## 5. Classroom Tips & Common Mistakes

| Pitfall | Prevention or Recovery |
| ------- | ---------------------- |
| Typo in a command | Re-type slowly, repeat the command clearly. Show `history` to re-run commands. |
| File not found errors (`No such file or directory`) | Verify with `ls` before running scripts. Explain uppercase/lowercase sensitivity. |
| Permission errors | If a command needs admin rights, explain why you won’t use `sudo` during class. Stick to project folder. |
| Poetry says dependency missing after install | Run `poetry install --sync` to force re-install. |
| API key not loading | Confirm `.env` spelling and run `cat .env`. Remind students not to share keys. |
| JSON looks messy | Use `head` or `jq` to show the top portion of the file. |

Encourage students to ask “What does this command do?” as you proceed—model curiosity and debugging discipline.

---

## 6. After-Class Follow-Up

1. Share the repository or a zip file so students can inspect the code.
2. Encourage them to modify the prompt template and re-run `process_outline.py`.
3. Suggest they explore simple changes (different entry ranges, adjusting `--temperature`, etc.) to build comfort.

---

## 7. Quick Reference Summary

```
mkdir -p ~/dev/NextGen
cd ~/dev/NextGen
git init
poetry init … (httpx, rich, python-dotenv)
# create Resources files
# create process_outline.py
python3 process_outline.py
# create nextgen_outline/cli.py
poetry install
poetry run nextgen-augment --help
poetry run nextgen-augment --entries 1-2
git add .
git commit -m "Initial outline tooling"
```

Keep this cheat sheet visible during the demo so you can glance at it if nerves kick in.

Good luck, and have fun showing law students how software can support their legal analysis! They will appreciate seeing mistakes handled gracefully, so narrate your thought process whenever something unexpected happens.

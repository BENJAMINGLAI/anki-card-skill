# Installing anki-expert for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed
- Python 3.10+ (for the `anki-export` CLI tool)

## Installation

1. **Install the export tool:**
   ```bash
   pip install git+https://github.com/gong1414/anki-card-skill.git
   ```

2. **Add the plugin** to `opencode.json` (global or project-level):
   ```json
   {
     "plugin": ["anki-expert@git+https://github.com/gong1414/anki-card-skill.git"]
   }
   ```

3. **Restart OpenCode.**

## Verify

Ask: "帮我做 Anki 卡片"

## Updating

Restart OpenCode to pull the latest version.

To pin a specific version:
```json
{
  "plugin": ["anki-expert@git+https://github.com/gong1414/anki-card-skill.git#v0.1.0"]
}
```

## Uninstalling

Remove the plugin line from `opencode.json` and restart OpenCode.

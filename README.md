# json2md

Turn messy JSON into readable Markdown — tables for arrays of objects, nested sections for objects, zero config.

## Install

```bash
pip install git+https://github.com/etailup/json2md.git
```

Or clone and install locally:

```bash
git clone https://github.com/etailup/json2md.git
cd json2md
pip install -e .
```

## Usage

```bash
# From a file
json2md response.json -t "Users API"

# From stdin
curl -s https://api.example.com/users | json2md -t Users

# Save to file
json2md package.json -o package.md
```

## Example

**Input**

```json
{
  "name": "json2md",
  "version": "0.1.0",
  "maintainers": [
    { "name": "Alex", "role": "author" },
    { "name": "Sam", "role": "contributor" }
  ]
}
```

**Output**

```markdown
# json2md

| Key | Value |
| --- | --- |
| name | json2md |
| version | 0.1.0 |

## maintainers

| name | role |
| --- | --- |
| Alex | author |
| Sam | contributor |
```

## Why

API responses, lockfiles, and config dumps are hard to skim. `json2md` gives you shareable docs in one command — useful for PRs, runbooks, and debugging.

## License

MIT

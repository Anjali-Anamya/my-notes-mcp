from pathlib import Path
from mcp.server.fastmcp import FastMCP

app = FastMCP("my-notes-mcp")
folder = Path("workspace")
folder.mkdir(exist_ok=True)


def checkpath(name: str) -> Path:
    if ".." in name:
        raise ValueError("Invalid path")
    return folder / name


@app.tool()
def listfiles() -> list[str]:
    """List all files in the workspace folder."""
    items = []
    for p in folder.rglob("*"):
        if p.is_file():
            items.append(str(p.relative_to(folder)))
    return items


@app.tool()
def readfile(name: str) -> str:
    """Read text from a file in the workspace folder."""
    file = checkpath(name)
    if not file.exists():
        return "File not found"
    return file.read_text(encoding="utf-8")


@app.tool()
def savenote(title: str, text: str) -> str:
    """Save a note as a markdown file inside workspace/notes."""
    notes = folder / "notes"
    notes.mkdir(exist_ok=True)
    clean = "".join(ch for ch in title.lower() if ch.isalnum() or ch == "-")
    if not clean:
        return "Bad title"
    target = checkpath(f"notes/{clean}.md")
    target.write_text(f"# {title}\n\n{text}\n", encoding="utf-8")
    return f"Saved {clean}.md"


@app.resource("workspace://count")
def filecount() -> str:
    """Return how many files are in the workspace."""
    total = sum(1 for p in folder.rglob("*") if p.is_file())
    return f"Total files: {total}"


if __name__ == "__main__":
    app.run()
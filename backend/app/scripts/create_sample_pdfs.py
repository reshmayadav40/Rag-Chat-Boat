from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas


DATA_DIR = Path(__file__).resolve().parents[2] / "data"

DOCUMENTS = {
    "react.pdf": [
        "React is a JavaScript library for building user interfaces.",
        "A component is a reusable part of a user interface.",
        "State lets a component remember information between renders.",
        "The useState Hook returns the current state and a function to update it.",
        "Calling the state update function causes React to render the component again.",
    ],
    "nodejs.pdf": [
        "Node.js is a JavaScript runtime that runs outside the browser.",
        "Express is a web framework commonly used with Node.js.",
        "Middleware is a function that can inspect a request and response during a request cycle.",
        "Middleware can authenticate users, log requests, or handle errors.",
        "A route handler sends a response when a request matches a route.",
    ],
    "mongodb.pdf": [
        "MongoDB is a document database that stores records as BSON documents.",
        "A collection is a group of related MongoDB documents.",
        "A document contains field and value pairs and is similar to a JSON object.",
        "An index helps MongoDB find matching documents more efficiently.",
        "A query specifies the documents that MongoDB should return.",
    ],
}


def create_pdf(path: Path, lines: list[str]) -> None:
    canvas = Canvas(str(path), pagesize=letter)
    width, height = letter
    y_position = height - 72

    canvas.setFont("Helvetica", 12)
    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            candidate = f"{current_line} {word}".strip()
            if canvas.stringWidth(candidate, "Helvetica", 12) > width - 144:
                canvas.drawString(72, y_position, current_line)
                y_position -= 20
                current_line = word
            else:
                current_line = candidate
        canvas.drawString(72, y_position, current_line)
        y_position -= 28

    canvas.save()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, lines in DOCUMENTS.items():
        create_pdf(DATA_DIR / filename, lines)
        print(f"Created {filename}")


if __name__ == "__main__":
    main()
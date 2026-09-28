from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas


DATA_DIR = Path(__file__).resolve().parents[2] / "data"

DOCUMENTS = {
    "react.pdf": [
        "React is a JavaScript library for building user interfaces.",
        "React is used to build reusable, interactive, and component-based user interfaces.",
        "A component is a reusable part of a user interface and can be written as a function.",
        "JSX lets developers write HTML-like markup inside JavaScript.",
        "Props are read-only inputs passed from a parent component to a child component.",
        "State lets a component remember information between renders.",
        "The useState Hook returns the current state and a function to update it.",
        "Calling a state update function causes React to render the component again.",
        "The useEffect Hook runs side effects such as data fetching, subscriptions, or timers.",
        "The dependency array controls when an effect runs again.",
        "Event handlers respond to actions such as clicks, typing, and form submission.",
        "Controlled inputs keep their value in React state.",
        "Conditional rendering displays different UI based on a condition.",
        "Lists are commonly rendered with the map function.",
        "Each item in a rendered list should have a stable key.",
        "React applications are commonly divided into small components for reuse and maintenance.",
        "The Virtual DOM helps React update the user interface efficiently.",
        "React does not provide a backend or database; it focuses on the user interface.",
        "React Router is commonly used to create multiple client-side pages.",
        "React can call an API with fetch and display the returned data.",
        "Context can share values such as themes or authenticated users across components.",
    ],
    "nodejs.pdf": [
        "Node.js is a JavaScript runtime that runs outside the browser.",
        "Node.js uses the V8 JavaScript engine.",
        "Node.js is commonly used for APIs, web servers, command-line tools, and real-time applications.",
        "Node.js uses an event loop and non-blocking I/O for handling many operations efficiently.",
        "Asynchronous code can use callbacks, Promises, or async and await.",
        "The npm package manager installs and manages JavaScript dependencies.",
        "package.json describes a Node.js project's scripts, dependencies, and metadata.",
        "The fs module reads and writes files, while the path module creates safe file paths.",
        "Express is a web framework commonly used with Node.js.",
        "An Express route connects an HTTP method and URL to a handler function.",
        "Middleware is a function that can inspect a request and response during a request cycle.",
        "Middleware can authenticate users, log requests, or handle errors.",
        "A route handler sends a response when a request matches a route.",
        "req contains request information and res is used to send a response.",
        "next passes control to the next middleware function.",
        "Express can parse JSON request bodies with express.json().",
        "HTTP GET reads data, POST creates data, PUT or PATCH updates data, and DELETE removes data.",
        "Environment variables keep configuration such as ports and secrets outside source code.",
        "Node.js can connect to databases through database drivers or application libraries.",
        "CORS controls which browser origins may call a server.",
    ],
    "mongodb.pdf": [
        "MongoDB is a document database that stores records as BSON documents.",
        "A collection is a group of related MongoDB documents.",
        "A document contains field and value pairs and is similar to a JSON object.",
        "MongoDB documents can contain nested objects and arrays.",
        "The _id field uniquely identifies a document and MongoDB creates it by default.",
        "MongoDB is schema-flexible, so documents in one collection can have different fields.",
        "A database contains collections, and collections contain documents.",
        "insertOne creates one document and insertMany creates multiple documents.",
        "find returns documents that match a filter and findOne returns the first matching document.",
        "updateOne and updateMany modify matching documents.",
        "deleteOne and deleteMany remove matching documents.",
        "The $set operator changes selected fields without replacing the whole document.",
        "The $inc operator increases or decreases a numeric field.",
        "An index helps MongoDB find matching documents more efficiently.",
        "The aggregation pipeline transforms and analyzes documents in multiple stages.",
        "The $match stage filters documents and the $group stage groups documents.",
        "MongoDB supports sorting, limiting, and projecting selected fields.",
        "Mongoose is an ODM library that provides schemas, models, validation, and middleware for MongoDB in Node.js.",
        "A Mongoose schema describes the shape and rules of application documents.",
        "A Mongoose model provides methods for creating, reading, updating, and deleting documents.",
        "MongoDB drivers allow applications to connect directly to a MongoDB server.",
    ],
}


def create_pdf(path: Path, lines: list[str]) -> None:
    canvas = Canvas(str(path), pagesize=letter)
    width, height = letter
    y_position = height - 72
    bottom_margin = 72
    line_height = 18
    paragraph_gap = 10

    canvas.setFont("Helvetica", 12)
    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            candidate = f"{current_line} {word}".strip()
            if canvas.stringWidth(candidate, "Helvetica", 12) > width - 144:
                if y_position < bottom_margin:
                    canvas.showPage()
                    canvas.setFont("Helvetica", 12)
                    y_position = height - 72
                canvas.drawString(72, y_position, current_line)
                y_position -= line_height
                current_line = word
            else:
                current_line = candidate

        if y_position < bottom_margin:
            canvas.showPage()
            canvas.setFont("Helvetica", 12)
            y_position = height - 72
        canvas.drawString(72, y_position, current_line)
        y_position -= line_height + paragraph_gap

    canvas.save()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, lines in DOCUMENTS.items():
        create_pdf(DATA_DIR / filename, lines)
        print(f"Created {filename}")


if __name__ == "__main__":
    main()
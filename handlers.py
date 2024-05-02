import json
import uuid
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from models import Note


class APIRequestHandler(BaseHTTPRequestHandler):
    parsed_url = urlparse("/")
    path = parsed_url.path

    def do_GET(self):
        if self.path.startswith("/api/notes") and self.command == "GET":
            notes = Note.all()
            if notes:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = {}
                for note in notes:
                    response = {"id": note[0], "title": note[1], "content": note[2]}
                    self.wfile.write(
                        json.dumps(response, sort_keys=False, indent=2).encode()
                    )
            else:
                self.send_response(404, "No note found")

        elif self.path.startswith("/api/notes/"):
            note_id = self.path.split("/")[-1]
            note = Note.get_by_id(note_id)
            if note:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(note).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()

    def do_POST(self):
        if self.path == "/api/notes" and self.command == "POST":
            content_length = int(self.headers["Content-Length"])
            note_data = json.loads(self.rfile.read(content_length))
            title = note_data.get("title", "")
            content = note_data.get("content", "")
            id = str(uuid.uuid4())
            if title and content:
                note = Note(id=id, title=title, content=content)
                note.save()
                self.send_response(201)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"message": "Post created successfully"}).encode()
                )

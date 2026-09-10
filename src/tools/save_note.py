SAVE_NOTE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "save_note",
        "description": "Save a note to a local text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The note content to save.",
                }
            },
            "required": ["content"],
        },
    },
}


def save_note(content: str) -> str:
    with open("notes.txt", "a", encoding="utf-8") as file:
        file.write(content + "\n")

    return "note saved"
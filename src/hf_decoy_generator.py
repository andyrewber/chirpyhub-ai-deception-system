from pathlib import Path
from transformers import pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DECOY_DIR = BASE_DIR / "docs" / "decoys"

# Hugging Face text generation pipeline
generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

PROMPTS = {
    "employee_notes.txt":
        "Write a short realistic employee workstation note:",

    "passwords.txt":
        "Write a fake but believable IT credential note:",

    "access_logs.txt":
        "Write realistic server access log entries:",

    "event_logs.txt":
        "Write realistic Windows event log entries:",

    "db_connection.txt":
        "Write a realistic internal database connection note:",

    "workstation_todo.txt":
        "Write a realistic IT workstation to-do list:"
}


def generate_content(prompt: str) -> str:
    result = generator(
        prompt,
        max_length=120,
        num_return_sequences=1,
        temperature=0.9
    )

    return result[0]["generated_text"]


def find_target_files():
    targets = []

    for file_path in DECOY_DIR.rglob("*"):
        if file_path.is_file():
            if file_path.name in PROMPTS:
                targets.append(file_path)

    return targets


def update_decoy_files():
    files = find_target_files()

    if not files:
        print("No matching decoy files found.")
        return

    for file_path in files:
        prompt = PROMPTS[file_path.name]

        print(f"\nGenerating AI content for: {file_path.name}")

        generated = generate_content(prompt)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(generated)

        print("Updated successfully.")


if __name__ == "__main__":
    update_decoy_files()
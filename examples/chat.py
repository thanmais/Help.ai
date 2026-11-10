"""Send one prompt to Groq using a local API key.

Copy .env.example to .env and paste your key from https://console.groq.com/keys
Then run:

    python chat.py "Explain fast language models in one sentence."
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def main() -> None:
    if not os.environ.get("GROQ_API_KEY"):
        print(
            "Missing GROQ_API_KEY. Copy .env.example to .env and paste your key."
        )
        sys.exit(1)

    prompt = " ".join(sys.argv[1:]).strip() or "Say hello in one sentence."
    model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")

    client = Groq()
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()

import requests

BACKEND_URL = "http://localhost:9000"


def main():
    # Start conversation
    start_res = requests.get(f"{BACKEND_URL}/start_conversation")
    start_res.raise_for_status()

    conversation = start_res.json()
    conversation_id = conversation["conversation_id"]

    print("Conversation ID:", conversation_id)
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Exiting the chat.")
            break

        payload = {
            "conversation_id": conversation_id,
            "message": user_input,
        }

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json=payload,
            timeout=30,
        )

        if response.status_code != 200:
            print("Error:", response.text)
            continue

        print("Assistant:", response.json().get("response"))


if __name__ == "__main__":
    main()
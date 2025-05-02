from dotenv import load_dotenv

load_dotenv()


def get_text_length(text: str) -> int:
    """
    Returns the length of the given text.
    """
    return len(text)

if __name__ == '__main__':
    print("Hello, World!")
    print(get_text_length("Dog"))
"""Simple Python starter for artificial-intelligence folder.

Run with: python -m artificial_intelligence.src.main
"""

def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to artificial-intelligence." 


def main() -> None:
    name = input("Enter your name: ")
    print(greet(name))


if __name__ == "__main__":
    main()

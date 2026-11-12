from Live import welcome, main_menu


def main():
    try:
        name = input("Enter your name: ")
        print(welcome(name))
        main_menu(name)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()


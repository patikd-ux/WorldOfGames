from Live import welcome, main_menu

try:
    name = input("Enter your name: ")
    print(welcome(name))
    main_menu()
except (KeyboardInterrupt, EOFError):
    print("\nGoodbye!")


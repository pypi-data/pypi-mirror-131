"""A simple library to ask the user for a password. Similar to getpass.getpass() but allows to specify a default mask (like '*' instead of blank)."""

__version__ = "0.5.5"

from sys import platform, stdin

if platform == "win32":
    from msvcrt import getch as __getch

    def getch():
        return __getch().decode()


else:
    # taken from https://stackoverflow.com/questions/1052107/reading-a-single-character-getch-style-in-python-is-not-working-in-unix
    from termios import tcgetattr, tcsetattr, TCSADRAIN
    from tty import setraw as tty_setraw

    def getch():
        old_settings = tcgetattr(stdin)
        try:
            tty_setraw(stdin)
            char = stdin.read(1)
        finally:
            tcsetattr(stdin, TCSADRAIN, old_settings)
        return char


def get_password(prompt="Password: ", mask="*"):
    print(prompt, end="", flush=True)

    password = ""
    while True:
        char = getch()

        # Enter
        if ord(char) == 13:
            print()
            break

        # Ctrl-C, Ctrl-D, Ctrl-Z
        elif ord(char) in [3, 4, 26]:
            exit(0)

        # Backspace, Delete
        elif ord(char) in [8, 127]:
            if len(password) > 0:
                print("\b \b", end="", flush=True)
                password = password[:-1]
        else:
            print(mask, end="", flush=True)
            password += char

    return password


if __name__ == "__main__":
    username = input("Username: ")
    password = get_password(mask="#")
    print(f"Username: {username}; Password: {password}")

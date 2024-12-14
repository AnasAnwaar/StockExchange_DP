import tkinter as tk
from src.ui.dashboard import Dashboard


class Application(tk.Tk):
    """
    Main application class for managing screens and navigation.
    """
    def __init__(self):
        super().__init__()
        self.title("ERP System")
        self.geometry("1920x1080")  # Full-screen dimensions
        self.attributes("-fullscreen", True)  # Enable full-screen mode

        # Stack to maintain navigation history
        self.screen_stack = []

        # Create a toolbar with window controls
        self.create_toolbar()

        # Frame container for switching between screens
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Start with the Dashboard screen
        self.show_screen(Dashboard)

    def create_toolbar(self):
        """
        Creates a toolbar with minimize, maximize, and close controls.
        """
        toolbar = tk.Frame(self, bg="lightgrey", height=30)
        toolbar.pack(fill="x", side="top")

        # Minimize Button
        minimize_button = tk.Button(
            toolbar, text="_", font=("Arial", 14), bg="lightgrey", command=self.iconify
        )
        minimize_button.pack(side="right", padx=5)

        # Maximize/Restore Button
        maximize_button = tk.Button(
            toolbar, text="□", font=("Arial", 12), bg="lightgrey",
            command=lambda: self.toggle_fullscreen()
        )
        maximize_button.pack(side="right", padx=5)

        # Close Button
        close_button = tk.Button(
            toolbar, text="X", font=("Arial", 14), bg="lightgrey", fg="red", command=self.quit
        )
        close_button.pack(side="right", padx=5)

    def toggle_fullscreen(self):
        """
        Toggles between fullscreen and windowed mode.
        """
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def show_screen(self, screen_class, *args, **kwargs):
        """
        Displays the given screen, replacing the current screen.
        :param screen_class: The class of the screen to display.
        :param args: Additional arguments for screen initialization.
        :param kwargs: Additional keyword arguments for screen initialization.
        """
        # Hide current screen if any
        if self.screen_stack:
            current_screen = self.screen_stack[-1]
            current_screen.pack_forget()

        # Check if the screen is already in the stack
        for screen in self.screen_stack:
            if isinstance(screen, screen_class):
                screen.pack(fill="both", expand=True)
                return

        # Create a new screen and add it to the stack
        screen = screen_class(self.container, self, *args, **kwargs)
        screen.pack(fill="both", expand=True)
        self.screen_stack.append(screen)

    def go_back(self):
        """
        Navigates to the previous screen in the history stack.
        """
        if len(self.screen_stack) > 1:
            # Hide the current screen
            current_screen = self.screen_stack.pop()
            current_screen.pack_forget()

            # Show the previous screen
            previous_screen = self.screen_stack[-1]
            previous_screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

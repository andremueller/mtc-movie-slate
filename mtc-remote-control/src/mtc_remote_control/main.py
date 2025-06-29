import tkinter as tk
from tkinter import ttk, messagebox
import sys

# --- Installation Check ---
# Try to import the required library and provide a helpful message if it's missing.
try:
    from pythonosc import udp_client
except ImportError:
    # Use messagebox for GUI-based error feedback
    # Fallback to console if Tkinter isn't ready yet.
    print("ERROR: The 'python-osc' library is not installed.")
    print(
        "Please install it by running this command in your terminal or command prompt:"
    )
    print("pip install python-osc")
    # A pop-up window is more user-friendly for a GUI app
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror(
        "Missing Library",
        "The 'python-osc' library is not installed.\n\nPlease run 'pip install python-osc' in your terminal and then restart the application.",
    )
    sys.exit(1)  # Exit the script


class OSCSenderApp(tk.Tk):
    """
    A simple Tkinter application to send OSC messages for production takes.
    """

    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("OSC Take Sender")
        self.geometry("450x450")  # Set a default size
        self.resizable(True, True)

        # --- Style Configuration ---
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # A clean, modern theme

        # --- Tkinter Data Variables ---
        # These variables link the GUI widgets to the underlying data.
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.StringVar(value="8000")
        self.production_var = tk.StringVar(value="My Production")
        self.part_var = tk.StringVar(value="Part 1")
        self.take_var = tk.IntVar(value=1)
        self.status_var = tk.StringVar(value="Ready. Configure and press Send.")

        # --- OSC Client ---
        # This will be initialized when the user sends a message.
        self.client = None

        # --- Initialize the UI ---
        self.create_widgets()
        
        self.send_osc_message()

    def create_widgets(self):
        """
        Creates and arranges all the GUI elements in the window.
        """
        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- OSC Configuration Section ---
        config_frame = ttk.LabelFrame(
            main_frame, text="OSC Target Configuration", padding="10"
        )
        config_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(config_frame, text="Target IP:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        ip_entry = ttk.Entry(config_frame, textvariable=self.ip_var, width=20)
        ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(config_frame, text="Target Port:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        port_entry = ttk.Entry(config_frame, textvariable=self.port_var, width=10)
        port_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # --- Production Info Section ---
        info_frame = ttk.LabelFrame(
            main_frame, text="Production Information", padding="10"
        )
        info_frame.pack(fill=tk.X, pady=10)

        ttk.Label(info_frame, text="Production Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        prod_entry = ttk.Entry(
            info_frame,
            textvariable=self.production_var,
            width=30,
            validate="focusout",
            validatecommand=self.send_osc_message
        )
        prod_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(info_frame, text="Part Name:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        part_entry = ttk.Entry(
            info_frame,
            textvariable=self.part_var,
            width=30,
            validate="focusout",
            validatecommand=self.send_osc_message
        )
        part_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # --- Take Control Section ---
        take_frame = ttk.Frame(info_frame)
        take_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(take_frame, text="Take Number:").pack(side=tk.LEFT, padx=5)

        take_entry = ttk.Entry(
            take_frame, textvariable=self.take_var, width=5, justify=tk.CENTER,
            validate="focusout",
            validatecommand=self.send_osc_message
        )
        take_entry.pack(side=tk.LEFT, padx=5)

        inc_button = ttk.Button(
            take_frame, text="+", width=2, command=self.increment_take
        )
        inc_button.pack(side=tk.LEFT)

        reset_button = ttk.Button(take_frame, text="Reset", command=self.reset_take)
        reset_button.pack(side=tk.LEFT, padx=5, fill=tk.X)

        # --- Action Button ---
        send_button = ttk.Button(
            main_frame, text="Send OSC Message", command=self.send_osc_message
        )
        send_button.pack(side=tk.BOTTOM, fill=tk.X)
        # , ipady=5, pady=10)
        # style="Accent.TButton",
        # self.style.configure("Accent.TButton", font=("Helvetica", 12, "bold"))

        # --- Status Bar ---
        status_bar = ttk.Label(
            self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def increment_take(self):
        """Increments the take number by 1."""
        self.take_var.set(self.take_var.get() + 1)
        # Automatically send message on increment
        self.send_osc_message()

    def reset_take(self):
        """Resets the take number to 1."""
        self.take_var.set(1)

    def send_osc_message(self):
        """
        Validates input, creates an OSC client, and sends the message.
        """
        # --- 1. Get and Validate Data ---
        ip_address = self.ip_var.get()
        try:
            port = int(self.port_var.get())
            if not (0 <= port <= 65535):
                raise ValueError("Port out of range")
        except ValueError:
            messagebox.showerror(
                "Invalid Port",
                f"The port '{self.port_var.get()}' is not a valid number (0-65535).",
            )
            self.status_var.set("Error: Invalid port number.")
            return

        production = self.production_var.get()
        part = self.part_var.get()
        take = self.take_var.get()

        # --- 2. Initialize OSC Client ---
        try:
            self.client = udp_client.SimpleUDPClient(ip_address, port)
        except Exception as e:
            messagebox.showerror("OSC Error", f"Could not create OSC client:\n{e}")
            self.status_var.set("Error: Could not connect.")
            return

        # --- 3. Send Messages ---
        # We will send each piece of data to a specific, namespaced OSC address.
        # This makes it easy to target specific labels in TouchOSC.
        try:
            # OSC Address, Value
            self.client.send_message("/production/name", production)
            self.client.send_message("/production/part", part)
            self.client.send_message("/production/take", take)

            status_message = f"Sent Take {take} to {ip_address}:{port}"
            print(status_message)  # Also print to console for logging
            self.status_var.set(status_message)

        except Exception as e:
            messagebox.showerror(
                "OSC Send Error", f"An error occurred while sending the message:\n{e}"
            )
            self.status_var.set("Error: Failed to send message.")


if __name__ == "__main__":
    # This block runs when the script is executed directly
    app = OSCSenderApp()
    app.mainloop()

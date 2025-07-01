import tkinter as tk
from tkinter import ttk, messagebox
import sys
import threading
import time
import socket

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

try:
    from zeroconf import ServiceBrowser, Zeroconf, ServiceListener
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Missing Library",
        "The 'zeroconf' library is not installed.\n\nPlease run 'pip install zeroconf' in your terminal and then restart the application."
    )
    sys.exit(1)


class TouchOSCListener(ServiceListener):
    """
    A listener for Zeroconf that collects information about TouchOSC services.
    It looks for services of type '_osc._tcp.local.'.
    """
    def __init__(self):
        super().__init__()
        self.services = []

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called by Zeroconf when a new service is discovered."""
        info = zc.get_service_info(type_, name)
        if info:
            # Decode address and get port
            address = socket.inet_ntoa(info.addresses[0])
            port = info.port
            # Store the service info
            self.services.append({"name": info.server, "address": address, "port": port})
            print(f"Discovered TouchOSC service: {info.server} at {address}:{port}")

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is updated (we don't need to act on this)."""
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is removed."""
        print(f"Service {name} removed")


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
        config_frame.columnconfigure(1, weight=1)

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

        # --- Discovery Button ---
        self.discover_button = ttk.Button(config_frame, text="Discover...", command=self.start_discovery)
        self.discover_button.grid(row=0, column=2, rowspan=2, padx=(10, 5), pady=5, sticky='ns')

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

    def start_discovery(self):
        """Starts the network discovery process in a separate thread."""
        self.discover_button.config(state=tk.DISABLED)
        self.status_var.set("Discovering services...")
        # Run discovery in a thread to not freeze the GUI
        discovery_thread = threading.Thread(target=self.run_discovery, daemon=True)
        discovery_thread.start()

    def run_discovery(self):
        """The core discovery logic that runs in a background thread."""
        zeroconf = Zeroconf()
        listener = TouchOSCListener()
        browser = ServiceBrowser(zeroconf, "_osc._tcp.local.", listener)
        
        # Wait for a few seconds to find services
        time.sleep(3)
        zeroconf.close()
        
        # Schedule the result handling back on the main GUI thread
        self.after(0, self.handle_discovery_results, listener.services)

    def handle_discovery_results(self, services):
        """Processes the list of discovered services in the main GUI thread."""
        self.discover_button.config(state=tk.NORMAL)
        if not services:
            self.status_var.set("Discovery finished. No services found.")
            messagebox.showinfo("Discovery", "No TouchOSC services were found on the network.")
        elif len(services) == 1:
            service = services[0]
            self.ip_var.set(service['address'])
            self.port_var.set(service['port'])
            self.status_var.set(f"Set target to {service['name'].replace('.local.', '')}")
        else:
            # If multiple services are found, show a selection dialog
            self.show_selection_dialog(services)

    def show_selection_dialog(self, services):
        """Creates a Toplevel window to let the user choose a service."""
        dialog = tk.Toplevel(self)
        dialog.title("Select a Device")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self) # Keep dialog on top of the main window
        
        ttk.Label(dialog, text="Multiple devices found. Please choose one:").pack(pady=10)
        
        listbox = tk.Listbox(dialog, height=5)
        listbox.pack(padx=10, pady=5, fill=tk.X)
        
        for service in services:
            # Display a user-friendly name
            display_name = service['name'].replace('.local.', '')
            listbox.insert(tk.END, display_name)

        def on_select():
            selection_index = listbox.curselection()
            if selection_index:
                selected_service = services[selection_index[0]]
                self.ip_var.set(selected_service['address'])
                self.port_var.set(selected_service['port'])
                self.status_var.set(f"Set target to {selected_service['name'].replace('.local.', '')}")
                dialog.destroy()

        select_button = ttk.Button(dialog, text="Select", command=on_select)
        select_button.pack(pady=10)
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        dialog.grab_set() # Modal behavior
        
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

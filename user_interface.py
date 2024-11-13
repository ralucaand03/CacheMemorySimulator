import tkinter as tk
from tkinter import ttk, messagebox

class UserInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cache Simulator Simulator")
        self.window.geometry("1080x600")
        self.window.configure(bg="#23967F")
        self.center_window()

        # Define color variables
        self.font_color_1 = "white"
        self.background_main = "#23967F"
        self.background_container = "#292F36"
        self.font_container = "Cascadia Code"
        self.btn_color = "#6874E8"

        # User input variables
        self.cache_size = tk.IntVar()
        self.address_width = tk.IntVar()
        self.block_size = tk.IntVar(value=2)
        self.associativity = tk.IntVar(value=1)
        self.write_hit_policy = tk.StringVar(value="write-back")
        self.write_miss_policy = tk.StringVar(value="write-allocate")
        self.replacement_policy = tk.StringVar(value="LRU")

        self.setup_ui()

    def center_window(self):
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Define the desired window size
        window_width = 1380
        window_height = 600

        # Calculate the position to center the window on the screen
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the window size and position
        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')


    def setup_ui(self):
        # Create main_container for left and right division
        main_container = ttk.Frame(self.window, padding="5", style="MainFrame.TFrame")  # Reduced padding
        main_container.grid(row=0, column=0, sticky="nsew")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Configure style
        style = ttk.Style()
        style.configure("MainFrame.TFrame", background=self.background_main)
        style.configure("ConfigFrame.TFrame", background=self.background_container)

        # Configure `container_left` (left side) inside main_container
        container_left = ttk.Frame(main_container, padding="5", style="MainFrame.TFrame")  # Reduced padding
        container_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Adjusted padding

        # Configure `container_right` (right side) inside main_container
        container_right = ttk.Frame(main_container, padding="5", style="MainFrame.TFrame")  # Reduced padding
        container_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Adjusted padding

        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)

        # Set up title in the first row of `container_left`
        title_label = ttk.Label(container_left, text="Cache Memory Simulator", font=("Doto", 28, "bold"), foreground="white", background=self.background_main)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")  # Reduced vertical padding

        # Create `background_container` with a colored background inside `container_left`
        background_container = ttk.Frame(container_left, padding="5", style="ConfigFrame.TFrame")  # Reduced padding
        background_container.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky="ew")  # Reduced padding

        # Set background color for the input container
        background_container.configure(style="InputFrame.TFrame")

        # Configure style for input container background
        style.configure("InputFrame.TFrame", background=self.background_container)

        # Add "Cache Configuration" title above the fields
        cache_config_title = ttk.Label(background_container, text="Cache Configuration", font=(self.font_container, 20), foreground=self.font_color_1, background=self.background_container)
        cache_config_title.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")  # Reduced vertical padding

        # Create `configuration_container` for input fields within `background_container`
        configuration_container = ttk.Frame(background_container, padding="5", style="ConfigFrame.TFrame")  # Reduced padding
        configuration_container.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky="ew")  # Reduced padding

        # Configure input fields within `configuration_container`
        entry_width = 20
        option_menu_width = 17
        
        ttk.Label(configuration_container, text="Cache Size (bytes):", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=0, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        tk.Entry(configuration_container, textvariable=self.cache_size, width=entry_width).grid(row=0, column=1)
        
        ttk.Label(configuration_container, text="Address Width (bits):", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=1, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        tk.Entry(configuration_container, textvariable=self.address_width, width=entry_width).grid(row=1, column=1)
        
        ttk.Label(configuration_container, text="Block Size (bytes):", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=2, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        
        block_size_menu = ttk.OptionMenu(configuration_container, self.block_size, 2, 2, 4, 8)
        block_size_menu.config(width=option_menu_width)
        block_size_menu.grid(row=2, column=1)
        
        ttk.Label(configuration_container, text="Associativity (ways):", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=3, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        associativity_menu = ttk.OptionMenu(configuration_container, self.associativity, 1, 1, 2, 4)
        associativity_menu.config(width=option_menu_width)
        associativity_menu.grid(row=3, column=1)
        
        ttk.Label(configuration_container, text="Write Hit Policy:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=4, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        write_hit_menu = ttk.OptionMenu(configuration_container, self.write_hit_policy, "write-back", "write-back", "write-through")
        write_hit_menu.config(width=option_menu_width)
        write_hit_menu.grid(row=4, column=1)
        
        ttk.Label(configuration_container, text="Write Miss Policy:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=5, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        write_miss_menu = ttk.OptionMenu(configuration_container, self.write_miss_policy, "write-allocate", "write-allocate", "no-write-allocate")
        write_miss_menu.config(width=option_menu_width)
        write_miss_menu.grid(row=5, column=1)
        
        ttk.Label(configuration_container, text="Replacement Policy:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=6, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        replacement_menu = ttk.OptionMenu(configuration_container, self.replacement_policy, "LRU", "LRU", "FIFO", "Random")
        replacement_menu.config(width=option_menu_width)
        replacement_menu.grid(row=6, column=1)

        # Place the `Run Simulation` button in the third row of `container_left`
        run_button = tk.Button(container_left, text="Run Simulation", command=self.run_simulation, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 12), padx=15, pady=8)
        run_button.grid(row=2, column=0, columnspan=2, pady=15)  # Adjusted padding

        # Add buttons for the different cache algorithms in `container_right`
        algorithm_buttons_frame = ttk.Frame(container_right, padding="5", style="MainFrame.TFrame")
        algorithm_buttons_frame.pack(padx=10, pady=10, fill="x")

        # Create the buttons for cache algorithms
        direct_mapped_button = tk.Button(algorithm_buttons_frame, text="Direct-Mapped Cache", command=self.direct_mapped_algorithm, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 10), padx=8, pady=5, width=24)  # Smaller padding, font size, and width
        direct_mapped_button.pack(side="left", padx=5)

        fully_associative_button = tk.Button(algorithm_buttons_frame, text="Fully Associative Cache", command=self.fully_associative_algorithm, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 10), padx=8, pady=5, width=24)  # Smaller padding, font size, and width
        fully_associative_button.pack(side="left", padx=5)

        set_associative_button = tk.Button(algorithm_buttons_frame, text="Set Associative Cache", command=self.set_associative_algorithm, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 10), padx=8, pady=5, width=24)  # Smaller padding, font size, and width
        set_associative_button.pack(side="left", padx=5)


        # Placeholder content for `container_right` (below buttons)
        placeholder_label = ttk.Label(container_right, text="Additional Features Here", font=(self.font_container, 14), background=self.background_container, foreground="white")
        placeholder_label.pack(expand=True)

    def direct_mapped_algorithm(self):
        messagebox.showinfo("Direct-Mapped Algorithm", "You have selected the Direct-Mapped Cache Algorithm.")

    def fully_associative_algorithm(self):
        messagebox.showinfo("Fully Associative Algorithm", "You have selected the Fully Associative Cache Algorithm.")

    def set_associative_algorithm(self):
        messagebox.showinfo("Set Associative Algorithm", "You have selected the Set Associative Cache Algorithm.")

    def run_simulation(self):
        results = {
            "Cache Size": self.cache_size.get(),
            "Address Width": self.address_width.get(),
            "Block Size": self.block_size.get(),
            "Associativity": self.associativity.get(),
            "Write Hit Policy": self.write_hit_policy.get(),
            "Write Miss Policy": self.write_miss_policy.get(),
            "Replacement Policy": self.replacement_policy.get(),
        }
        self.display_results(results)

    def display_results(self, results):
        result_text = "\n".join(f"{key}: {value}" for key, value in results.items())
        messagebox.showinfo("Simulation Results", result_text)

    def start(self):
        self.window.mainloop()

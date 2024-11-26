import tkinter as tk
from tkinter import ttk, messagebox
from simulation import Simulation
from direct_mapped_cache import Direct_mapped_cache
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
        self.color_pink= "#E56B70"
        self.font_container = "Cascadia Code"
        self.btn_color = "#6874E8"

        # User input variables
        self.cache_size = tk.IntVar(value=16)
        self.address_width = tk.IntVar(value=6)
        self.block_size = tk.IntVar(value=2)
        self.associativity = tk.IntVar(value=1)
        self.write_hit_policy = tk.StringVar(value="write-back")
        self.write_miss_policy = tk.StringVar(value="write-allocate")
        self.replacement_policy = tk.StringVar(value="LRU")
        self.instuction = tk.StringVar(value="LOAD")
        self.capacity = tk.IntVar(value = 4)
        self.input = tk.StringVar(value ="1,2,3")
        self.dir = 0
        self.binary_value = 0
        self.text_boxes = [] 
        self.setup_ui()

    def center_window(self):
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        window_width = 1380
        window_height = 600

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')


    def setup_ui(self):
        # Create main_container for left and right division
        main_container = ttk.Frame(self.window, padding="5", style="MainFrame.TFrame")
        main_container.grid(row=0, column=0, sticky="nsew")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Configure style
        style = ttk.Style()
        style.configure("MainFrame.TFrame", background=self.background_main)
        style.configure("ConfigFrame.TFrame", background=self.background_container)

        # Configure `container_left` (left side) inside main_container
        container_left = ttk.Frame(main_container, padding="5", style="MainFrame.TFrame") 
        container_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  

        # Configure `container_right` (right side) inside main_container
        container_right = ttk.Frame(main_container, padding="5", style="MainFrame.TFrame") 
        container_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") 

        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)

        # Set up title in the first row of `container_left`
        title_label = ttk.Label(container_left, text="Cache Memory Simulator", font=("Doto", 28, "bold"), foreground="white", background=self.background_main)
        title_label.grid(row=0, column=0, columnspan=2, pady=(15, 20), sticky="ew") 

        # Create `background_container` with a colored background inside `container_left`
        background_container = ttk.Frame(container_left, padding="5", style="ConfigFrame.TFrame")  
        background_container.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky="ew")  

        # Set background color for the input container
        background_container.configure(style="InputFrame.TFrame")

        # Configure style for input container background
        style.configure("InputFrame.TFrame", background=self.background_container)

        # Add "Cache Configuration" title above the fields
        cache_config_title = ttk.Label(background_container, text="Cache Configuration", font=(self.font_container, 20), foreground=self.font_color_1, background=self.background_container)
        cache_config_title.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")  

        # Create `configuration_container` for input fields within `background_container`
        self.configuration_container = ttk.Frame(background_container, padding="5", style="ConfigFrame.TFrame") 
        self.configuration_container.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky="ew") 

        # Configure input fields within `configuration_container`
        entry_width = 22
        option_menu_width = 17

        ttk.Label(self.configuration_container, text="Cache Size (bytes):", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=0, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        tk.Entry(self.configuration_container, textvariable=self.cache_size, width=entry_width).grid(row=0, column=1)

        ttk.Label(self.configuration_container, text="Address Width (bits):", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=1, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        tk.Entry(self.configuration_container, textvariable=self.address_width, width=entry_width).grid(row=1, column=1)

        ttk.Label(self.configuration_container, text="Block Size (bytes):", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=2, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding

        block_size_menu = ttk.OptionMenu(self.configuration_container, self.block_size, 2, 2, 4, 8)
        block_size_menu.config(width=option_menu_width)
        block_size_menu.grid(row=2, column=1)

        ttk.Label(self.configuration_container, text="Write Hit Policy:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=3, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        write_hit_menu = ttk.OptionMenu(self.configuration_container, self.write_hit_policy, "write-back", "write-back", "write-through")
        write_hit_menu.config(width=option_menu_width)
        write_hit_menu.grid(row=3, column=1)

        ttk.Label(self.configuration_container, text="Write Miss Policy:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=4, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        write_miss_menu = ttk.OptionMenu(self.configuration_container, self.write_miss_policy, "write-allocate", "write-allocate", "no-write-allocate")
        write_miss_menu.config(width=option_menu_width)
        write_miss_menu.grid(row=4, column=1)

        ttk.Label(self.configuration_container, text="Replacement Policy:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=5, column=0, sticky=tk.W, pady=3)  # Reduced vertical padding
        replacement_menu = ttk.OptionMenu(self.configuration_container, self.replacement_policy, "LRU", "LRU", "FIFO", "Random")
        replacement_menu.config(width=option_menu_width)
        replacement_menu.grid(row=5, column=1)

        ttk.Label(self.configuration_container, text=".....................", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=6, column=0, sticky=tk.W, pady=3)
        ttk.Label(self.configuration_container, text="..............", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=6, column=1, sticky=tk.W, pady=3)
       

        ttk.Label(self.configuration_container, text="Capacity:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=7, column=0, sticky=tk.W, pady=3)
        tk.Entry(self.configuration_container, textvariable=self.capacity, width=entry_width).grid(row=7, column=1)


        # Place the "Input" label and entry in the next row
        ttk.Label(self.configuration_container, text="Input:", font=(self.font_container, 14), foreground=self.font_color_1, background=self.background_container).grid(row=8, column=0, sticky=tk.W, pady=3)
        tk.Entry(self.configuration_container, textvariable=self.input, width=entry_width).grid(row=8, column=1)

        # Place the `Run Simulation` button in the third row of `container_left`
        run_button = tk.Button(container_left, text="Run Simulation", command=self.run_simulation, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 12), padx=15, pady=8)
        run_button.grid(row=2, column=0, columnspan=2, pady=15) 

        # Add buttons for the different cache algorithms in `container_right`
        algorithm_buttons_frame = ttk.Frame(container_right, padding="16", style="MainFrame.TFrame")
        algorithm_buttons_frame.grid(row=0, column=0, pady=(8,10), sticky="n")  

        # Create the buttons for cache algorithms
        direct_mapped_button = tk.Button(algorithm_buttons_frame, text="Direct-Mapped Cache", command=self.direct_mapped_algorithm, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 10), padx=8, pady=5, width=30)
        direct_mapped_button.grid(row=0, column=0, padx=5)

        fully_associative_button = tk.Button(algorithm_buttons_frame, text="Fully Associative Cache", command=self.fully_associative_algorithm, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 10), padx=8, pady=5, width=30)
        fully_associative_button.grid(row=0, column=1, padx=5)

        set_associative_button = tk.Button(algorithm_buttons_frame, text="Set Associative Cache", command=self.set_associative_algorithm, bg=self.btn_color, fg="white", activebackground="#505FC4", activeforeground="white", font=(self.font_container, 10), padx=8, pady=5, width=30)
        set_associative_button.grid(row=0, column=2, padx=5)
        
        rightrow = ttk.Frame(container_right, padding="5", style="ConfigFrame.TFrame")  
        rightrow.grid(row=1, column=0, padx=5, pady=0, sticky="nsew")  
        # Create `output_container` for cache output
        self.output_container = ttk.Frame(rightrow, padding="2", style="ConfigFrame.TFrame")
        self.output_container.grid(row=0, column=0, sticky="nsew")

        # Create `main_memory_container` for main memory output
        self.main_memory_container = ttk.Frame(rightrow, padding="0", style="ConfigFrame.TFrame")
        self.main_memory_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)  
        rightrow.grid_columnconfigure(1, weight=0)

        cache_table = ttk.Frame(container_right, padding="5", style="ConfigFrame.TFrame")  
        cache_table.grid(row=2, column=0, padx=5, pady=0, sticky="nsew")  

        # Configure `container_right` rows and columns
        container_right.grid_rowconfigure(0, weight=1)
        container_right.grid_rowconfigure(1, weight=18) 
        
        self.cache_memory_container = ttk.Frame(container_right, padding="0", style="ConfigFrame.TFrame")
        self.cache_memory_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=15)  

#---------------------------------------------------------------------------------------------------------------------

    def direct_mapped_algorithm(self):
        self.cache = Direct_mapped_cache(self)
        self.cache.direct_mapped()
        ttk.Label(self.configuration_container,text="Instruction:",font=(self.font_container, 14),foreground=self.font_color_1,background=self.background_container).grid(row=7, column=0, sticky=tk.W, pady=3)
        instruction_menu = ttk.OptionMenu( self.configuration_container,self.instuction,   "LOAD","LOAD", "STORE")
        instruction_menu.config(width=17) 
        instruction_menu.grid(row=7, column=1)  
        self.input.set("hex,hex") 
        self.dir = 1

    def fully_associative_algorithm(self):
        messagebox.showinfo("Fully Associative Algorithm", "You have selected the Fully Associative Cache Algorithm.")

    def set_associative_algorithm(self):
        messagebox.showinfo("Set Associative Algorithm", "You have selected the Set Associative Cache Algorithm.")

    def display_results(self, results):
        result_text = "\n".join(f"{key}: {value}" for key, value in results.items())
        messagebox.showinfo("Simulation Results", result_text)

    def start(self):
        self.window.mainloop()

    def create_frame_labels(self, capacity):
        for frame_label in getattr(self, "frame_labels", []):
            frame_label.destroy()
        self.frame_labels = []
        for i in range(capacity):
            frame_label = tk.Label(self.output_container, width=11, height=2,font=("Cascadia Code", 14),bg="white",relief="solid",borderwidth=1
            )
            frame_label.grid(row=i // 6, column=i%6, pady=5, padx=5, sticky="nsew")
            self.frame_labels.append(frame_label)

    def update_canvas(self, current_page, cache):
            for frame_label in self.frame_labels:
                frame_label.config(bg="white", text="")
            for i, page in enumerate(cache):
                if i < len(self.frame_labels):
                    if current_page == page:
                        self.frame_labels[i].config(bg=self.background_main, text=str(page))  # Cache hit 
                    else:
                        self.frame_labels[i].config(bg=self.color_pink, text=str(page))  # Cache miss

    def input_split(self, input_sequence):
        try:
            return list(map(lambda x: int(x.strip()), input_sequence.split(',')))
        except ValueError as e:
            print(f"Error: Invalid input. Ensure all entries are integers. Details: {e}")
            return []

    def input_split(self, input_sequence):
        try:
            # Parse input as hexadecimal strings
            return list(map(lambda x: x.strip(), input_sequence.split(',')))
        except Exception as e:
            print(f"Error: Invalid input. Ensure all entries are valid hexadecimal strings. Details: {e}")
            return []
        
    def remove_first_value(self,input_str):
        values = input_str.split(',')
        values.pop(0)
        return ','.join(values)

    def run_simulation(self):
        if self.dir == 0:
            simulation = Simulation(self)
            simulation.run_simulation()
        elif self.dir == 1:
            if self.instuction.get() == "LOAD":
                input_sequence = self.input.get()  
                if not input_sequence.strip():  
                    print("Input is empty. Please enter valid data.")
                    return
                hex_values = self.input_split(input_sequence)
                if hex_values:  
                    try:
                        first_value = int(hex_values[0], 16) 
                        binary_value = bin(first_value)[2:]  
                    except ValueError as e:
                        print(f"Error converting hexadecimal to binary. Details: {e}")
                else:
                    print("No valid hexadecimal values to process.")
                
                self.cache.load_instruction(binary_value)
                self.input.set(self.remove_first_value(input_sequence)) 
                

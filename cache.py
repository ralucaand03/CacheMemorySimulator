import tkinter as tk
from tkinter import ttk, messagebox
class Cache:
    def __init__(self, ui):
        self.ui = ui
        self.cache_size = ui.cache_size.get()
        self.block_size = ui.block_size.get()
        self.address_width = ui.address_width.get()
        self.write_hit_policy = ui.write_hit_policy.get()
        self.write_miss_policy = ui.write_miss_policy.get()
        self.replacement_policy = ui.replacement_policy.get()
        self.cache_data = {}

        # Declare the variables for direct-mapped cache simulation
        self.num_blocks = 0
        self.block_offset_bits = 0
        self.index_bits = 0
        self.tag_bits = 0
#---------------------------------------------------------------------------------------------------------------------

    def direct_mapped(self):
        if not self.validate():
            return 
        
        self.num_blocks = self.cache_size // self.block_size
        self.block_offset_bits = (self.block_size - 1).bit_length()  # log2(block_size)
        self.index_bits = (self.num_blocks - 1).bit_length()  # log2(number of blocks)
        self.tag_bits = self.address_width - (self.index_bits + self.block_offset_bits)

        print(f"Direct-Mapped Cache Simulation:")
        print(f"Number of blocks: {self.num_blocks}")
        print(f"Tag bits: {self.tag_bits}")
        print(f"Index bits: {self.index_bits}")
        print(f"Block offset bits: {self.block_offset_bits}")

        for widget in self.ui.output_container.winfo_children():
            widget.destroy()
        title_label = tk.Label(
            self.ui.output_container,
            text="Instruction Breakdown",
            font=("Cascadia Code", 16, "bold"),
            bg=self.ui.background_container,
            fg=self.ui.font_color_1
        )
        title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=(10, 5), sticky="W")

        headers = ["Tag", "Index", "Offset"]
        for col, header in enumerate(headers):
            header_label = tk.Label(
                self.ui.output_container,
                text=header,
                width=12,
                height=2,
                font=("Cascadia Code", 14, "bold"),
                bg=self.ui.background_main,
                fg=self.ui.font_color_1,
                relief="solid",
                borderwidth=1
            )
            header_label.grid(row=1, column=col, padx=5, pady=7, sticky="nsew")

        zeros = ['0' * self.tag_bits, '0' * self.index_bits, '0' * self.block_offset_bits]
        for col, value in enumerate(zeros):
            row_label = tk.Label(
                self.ui.output_container,
                text=value,
                width=12,
                height=2,
                font=("Cascadia Code", 14),
                bg=self.ui.font_color_1,
                fg=self.ui.background_main,
                relief="solid",
                borderwidth=0.2
            )
            row_label.grid(row=2, column=col, padx=5, pady=0, sticky="nsew")
            self.create_main_memory_table()
#---------------------------------------------------------------------------------------------------------------------

    def create_main_memory_table(self):
        try:
            # Read data from main_memory.txt
            with open("main_memory.txt", "r") as file:
                lines = file.readlines()

            if not lines:
                messagebox.showerror("Error", "main_memory.txt is empty.")
                return

            max_rows = self.cache_size * 4
            rows_to_display = lines[:max_rows]

            for widget in self.ui.main_memory_container.winfo_children():
                widget.destroy()

            # Add label above the table
            title_label = tk.Label(
                self.ui.main_memory_container,
                text="Memory Block",
                font=("Cascadia Code", 16, "bold"),
                bg=self.ui.background_container,
                fg=self.ui.font_color_1
            )
            title_label.pack(side="top", anchor="ne", pady=(10, 14), padx=10)  # Position label on the top-right

            # Create the frame for the table
            frame = tk.Frame(self.ui.main_memory_container)
            frame.pack(fill="both", expand=True)

            
            canvas = tk.Canvas(frame, height=  40, width=340)  # Set precise canvas dimensions
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=False)
            scrollbar.pack(side="right", fill="y")

            for i, line in enumerate(rows_to_display):
                address, data = line.strip().split(", ")
                label_address = ttk.Label(scrollable_frame, text=address, width=10, anchor="center")
                label_data = ttk.Label(scrollable_frame, text=data, width=10, anchor="center")

                # Add to grid
                label_address.grid(row=i, column=0, padx=2, pady=2, sticky="nsew")
                label_data.grid(row=i, column=1, padx=2, pady=2, sticky="nsew")

        except FileNotFoundError:
            messagebox.showerror("Error", "main_memory.txt not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

#---------------------------------------------------------------------------------------------------------------------
    def validate(self):
        if self.cache_size <= 0 or self.block_size <= 0 or self.address_width <= 0:
            messagebox.showerror("Input Error", "Cache size, block size, and address width must be positive integers.")
            return False
        if self.block_size & (self.block_size - 1) != 0:
            messagebox.showerror("Input Error", "Block size must be a power of 2.")
            return False
        if self.cache_size % self.block_size != 0:
            messagebox.showerror("Input Error", "Cache size must be a multiple of block size.")
            return False
        if self.address_width < self.cache_size.bit_length():
            messagebox.showerror("Input Error", "Address width must be large enough to address the entire cache size.")
            return False
        return 
    

    # Load = Read. Retrieves data from memory/cache.
    # Store = Write. Saves data to memory/cache.


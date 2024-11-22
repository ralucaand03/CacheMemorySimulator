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
            # Total memory size derived from address width
            total_memory_size = 2 ** self.address_width  # Example: 2^8 = 256 for 8-bit addresses
            total_blocks = total_memory_size // self.block_size  # Total number of memory blocks

            # Clear any existing widgets in the container
            for widget in self.ui.main_memory_container.winfo_children():
                widget.destroy()

            # Add label above the table
            title_label = tk.Label(
                self.ui.main_memory_container,
                text="Main Memory",
                font=("Cascadia Code", 16, "bold"),
                bg=self.ui.background_container,
                fg=self.ui.font_color_1
            )
            title_label.pack(side="top", anchor="ne", pady=(10, 14), padx=10)

            # Create the frame for the table
            frame = tk.Frame(self.ui.main_memory_container)
            frame.pack(fill="both", expand=True)

            # Set up canvas and scrollbars with fixed height and width
            canvas = tk.Canvas(frame, height=40, width=340)
            vertical_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            # Create the scrollable window and set scrollbars
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

            canvas.grid(row=0, column=0, sticky="nsew")
            
            vertical_scrollbar.grid(row=0, column=1, sticky="ns")

            horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

            # Generate main memory dynamically and display it in blocks and words
            word_counter = 0
            for block in range(total_blocks):
                for word in range(self.block_size):
                    word_label = ttk.Label(
                        scrollable_frame, 
                        text=f"B{block}W{word_counter}", 
                        width=10, 
                        anchor="center"
                    )
                    word_label.grid(
                        row=(block * 2) + 1, column=word, padx=5, pady=2, sticky="nsew"
                    )
                    word_counter += 1

            canvas.update_idletasks() 

            if canvas.bbox("all")[3] > frame.winfo_height():
                vertical_scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                vertical_scrollbar.grid_forget()

            if canvas.bbox("all")[2] > frame.winfo_width():
                horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
            else:
                horizontal_scrollbar.grid_forget()

            frame.grid_columnconfigure(0, weight=0)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_rowconfigure(1, weight=0) 
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
        if self.address_width > 10 :
            messagebox.showerror("Input Error", "Address width must be max 10")
            return False
        return True
    

    # Load = Read. Retrieves data from memory/cache.
    # Store = Write. Saves data to memory/cache.

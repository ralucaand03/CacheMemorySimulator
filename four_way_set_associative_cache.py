import tkinter as tk
import random
from collections import deque
from tkinter import ttk, messagebox
class Four_way_set_associative_cache:
    def __init__(self, ui):
        self.ui = ui
        self.cache_size = ui.cache_size.get()
        self.block_size = ui.block_size.get()
        self.address_width = ui.address_width.get()
        self.write_hit_policy = ui.write_hit_policy.get()
        self.write_miss_policy = ui.write_miss_policy.get()
        self.replacement_policy = ui.replacement_policy.get()
        self.cache_data = {}
        self.cache_contents = []
        self.main_contents = []
        self.main_canvas = None
        self.cache_title_label= "Cache Memory"
        self.tio_label = "Instruction Breakdown"
        
        self.replacement_array = [deque(range(4)) for _ in range(self.cache_size // self.block_size //4)]
        self.num_blocks = 0
        self.num_sets = 0
        self.block_offset_bits = 0
        self.index_bits = 0
        self.tag_bits = 0
        self.tag = '0'
        self.index = '0'
        self.offset = '0'
        self.data_byte = ""

#---------------------------------------------------------------------------------------------------------------------
    def four_way_set_associative(self):
        if not self.validate():
            return
        
        # Calculate the number of blocks and sets for the 4-way set-associative cache
        self.num_blocks = self.cache_size // self.block_size
        self.num_sets = self.num_blocks // 4  # 4-way set-associative cache (4 cache lines per set)
        
        # Number of bits for block offset
        self.block_offset_bits = (self.block_size - 1).bit_length()
        
        # Number of bits for index (based on the number of sets)
        self.index_bits = (self.num_sets - 1).bit_length()
        
        # Number of bits for tag
        self.tag_bits = self.address_width - (self.index_bits + self.block_offset_bits)

        print(f":::::::::::::::::::::::::::::::::::")
        print(f"4-Way Set-Associative Cache Simulation:")
        print(f"Cache size: {self.cache_size}")
        print(f"Address width: {self.address_width}")
        print(f"Block size: {self.block_size}")
        print(f"Number of blocks: {self.num_blocks}")
        print(f"Number of sets: {self.num_sets}")
        print(f"Tag bits: {self.tag_bits}")
        print(f"Index bits: {self.index_bits}")
        print(f"Block offset bits: {self.block_offset_bits}")
        print("------------------------------------")
        
        for widget in self.ui.output_container.winfo_children():
            widget.destroy()
        
        # Instruction Breakdown Label
        self.tio_label = tk.Label(
            self.ui.output_container,
            text="Instruction Breakdown",
            font=("Cascadia Code", 16, "bold"),
            bg=self.ui.background_container,
            fg=self.ui.font_color_1
        )
        self.tio_label.grid(row=0, column=0, columnspan=3, padx=5, pady=(10, 5), sticky="W")
        
        # Create headers for the instruction breakdown
        headers = ["Tag", "Set Index", "Offset"]
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

        # Display the default values (all zeroes) for tag, index, and offset
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
        self.create_cache_table()

#---------------------------------------------------------------------------------------------------------------------
    def update_tio(self, binary_number):
        binary_zero = bin(0)[2:].zfill(self.address_width)
        binary_number = binary_number.zfill(self.address_width)
        
        # Split the address into Tag, Index, and Offset
        self.tag = binary_number[:self.tag_bits]
        self.index = binary_number[self.tag_bits:self.tag_bits + self.index_bits]
        self.offset = binary_number[self.tag_bits + self.index_bits:]

        # Print the breakdown for debugging (optional)
        if binary_number != binary_zero:
            print(f"Tag: {self.tag}")
            print(f"Set Index: {self.index}")
            print(f"Offset: {self.offset}")
        
        # Update the UI to reflect the new values
        for widget in self.ui.output_container.winfo_children():
            if int(widget.grid_info()['row']) == 2:
                widget.destroy()

        # Display the updated tag, index, and offset
        values = [self.tag, self.index, self.offset]
        for col, value in enumerate(values):
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

#---------------------------------------------------------------------------------------------------------------------
    def create_main_memory_table(self):
        try:
            total_memory_size = 2 ** self.address_width
            total_blocks = total_memory_size // self.block_size  # Total number of memory blocks

            for widget in self.ui.main_memory_container.winfo_children():
                widget.destroy()
            self.main_contents.clear()
            title_label = tk.Label(
                self.ui.main_memory_container,
                text="Main Memory",
                font=("Cascadia Code", 16, "bold"),
                bg=self.ui.background_container,
                fg=self.ui.font_color_1
            )
            title_label.pack(side="top", anchor="ne", pady=(10, 14), padx=10)

            frame = tk.Frame(self.ui.main_memory_container)
            frame.pack(fill="both", expand=True)

            self.main_canvas = tk.Canvas(frame, height=40, width=350)
            vertical_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.main_canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.main_canvas.xview)
            self.main_scrollable_frame = ttk.Frame(self.main_canvas)

            self.main_scrollable_frame.bind(
                "<Configure>",
                lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            )

            self.main_canvas.create_window((0, 0), window=self.main_scrollable_frame, anchor="nw")
            self.main_canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

            self.main_canvas.grid(row=0, column=0, sticky="nsew")

            vertical_scrollbar.grid(row=0, column=1, sticky="ns")
            horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

            # Create a ttk.Style instance and configure the style for labels
            style = ttk.Style()
            style.configure("MemoryLabel.TLabel", 
                            foreground=self.ui.color_pink,  # Set the foreground color
                            background=self.ui.font_color_1,  # Set the background color
                            font=("Cascadia Code", 10))

            # Create labels and populate main_contents
            word_counter = 0
            for block in range(total_blocks):
                block_data = []  # Temporary list to store the current block's data
                for word in range(self.block_size):
                    label_text = f"B{block}W{word_counter}"
                    word_label = ttk.Label(
                        self.main_scrollable_frame,
                        text=label_text,
                        width=10,
                        anchor="center",
                        style="MemoryLabel.TLabel"  # Apply the custom style
                    )
                    word_label.grid(
                        row=(block * 2) + 1, column=word, padx=5, pady=2, sticky="nsew"
                    )
                    block_data.append(label_text)  # Store the text of the label
                    word_counter += 1
                self.main_contents.append(block_data)  # Append the block's data to main_contents

            self.main_canvas.update_idletasks()

            if self.main_canvas.bbox("all")[3] > frame.winfo_height():
                vertical_scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                vertical_scrollbar.grid_forget()

            if self.main_canvas.bbox("all")[2] > frame.winfo_width():
                horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
            else:
                horizontal_scrollbar.grid_forget()

            frame.grid_columnconfigure(0, weight=0)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_rowconfigure(1, weight=0)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_main_memory_table(self, search_index=None):
        try:
            # Ensure main_contents and main_scrollable_frame exist
            if not hasattr(self, "main_contents") or not self.main_contents:
                raise AttributeError("Main memory contents not initialized. Please create the main memory table first.")
            if not hasattr(self, "main_scrollable_frame") or self.main_scrollable_frame is None:
                raise AttributeError("Main memory scrollable frame not initialized.")

            # Clear existing widgets in the scrollable frame
            for widget in self.main_scrollable_frame.winfo_children():
                widget.destroy()

            # Create or configure styles for highlighting and default labels
            style = ttk.Style()
            style.configure("DefaultLabel.TLabel", 
                            foreground=self.ui.color_pink,  # Set the foreground color
                            background=self.ui.font_color_1,  # Set the background color
                            font=("Cascadia Code", 10))
            style.configure("HighlightLabel.TLabel", 
                            background="yellow", 
                            foreground="black")

            # Recreate the table using updated contents
            for block_index, block_data in enumerate(self.main_contents):
                # Validate block data length
                if len(block_data) != self.block_size:
                    raise ValueError(f"Block {block_index} has an incorrect number of elements. Expected {self.block_size}, found {len(block_data)}.")
                for word_index, word_data in enumerate(block_data):
                    # Choose style based on search_index
                    style_to_use = "HighlightLabel.TLabel" if search_index == block_index else "DefaultLabel.TLabel"

                    word_label = ttk.Label(
                        self.main_scrollable_frame,
                        text=str(word_data),  # Convert to string for display
                        width=10,
                        anchor="center",
                        style=style_to_use
                    )
                    word_label.grid(
                        row=(block_index * 2) + 1, column=word_index, padx=5, pady=2, sticky="nsew"
                    )

        except Exception as e:
            print(f"Error in update_main_memory_table: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
 
    def color_main_memory_row(self, row, bg_color, fg_color):
        try:
            # Reset all rows to their default color
            for widget in self.main_scrollable_frame.winfo_children():
                grid_info = widget.grid_info()
                widget_row = int(grid_info['row'])  # Get the row index of the widget

                if isinstance(widget, ttk.Label):
                    # Reset to default style
                    widget.config(
                        background=self.ui.font_color_1,  
                        foreground=self.ui.color_pink,
                    )
            if row != None:
                
                for widget in self.main_scrollable_frame.winfo_children():
                    grid_info = widget.grid_info()
                    widget_row = int(grid_info['row'])  # Get the row index of the widget
                    
                    # Check if this widget belongs to the specified row
                    if widget_row == (row * 2) + 1:  # Adjust for grid layout (row * 2) + 1 is the actual content row
                        # Set the style for background and foreground color
                        widget.config(background=bg_color, foreground=fg_color)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while coloring the main memory row: {e}")
#---------------------------------------------------------------------------------------------------------------------
    def create_cache_table(self):
        try:
            # Clear any previous cache content
            for widget in self.ui.cache_memory_container.winfo_children():
                widget.destroy()

            # Title for Cache Memory section
            self.cache_title_label = tk.Label(self.ui.cache_memory_container, text="Cache Memory", font=("Cascadia Code", 16, "bold"), bg=self.ui.background_container, fg=self.ui.font_color_1)
            self.cache_title_label.pack(side="top", anchor="nw", pady=(10, 5), padx=5)
            self.cache_contents.clear()

            # Create a frame for the cache memory table
            frame = tk.Frame(self.ui.cache_memory_container)
            frame.pack(fill="both", expand=True)

            # Set up canvas and scrollbars for better visualization
            canvas = tk.Canvas(frame, height=210, width=280)
            vertical_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            self.cache_scrollable_frame = ttk.Frame(canvas)

            # Configure scrollable area
            self.cache_scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            # Create window inside the canvas
            canvas.create_window((0, 0), window=self.cache_scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=vertical_scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            vertical_scrollbar.pack(side="right", fill="y")

            # Define headers for the cache memory table
            headers = ["Set", "Valid", "Tag"] + [f"Byte{i}" for i in range(self.block_size)] + ["Dirty"]
            for col, header in enumerate(headers):
                header_label = tk.Label(self.cache_scrollable_frame, text=header, width=6, height=1, font=("Cascadia Code", 10, "bold"),
                                        bg=self.ui.background_main, fg=self.ui.font_color_1, relief="solid", borderwidth=1)
                header_label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

            # Create the rows for the cache table (adjusted for 4-way set-associative cache)
            for set_idx in range(self.num_sets):  # Iterate over the sets
                for line_idx in range(4):  # Each set has 4 cache lines (4-way set-associative)
                    row = set_idx * 4 + line_idx  # Row number (cache line)

                    # List to hold row content for each cache line
                    row_data = []

                    # Set column: Show the set index
                    set_value = f"{set_idx}"
                    bg_color = self.ui.row_color if set_idx % 2 == 1 else self.ui.font_color_1  # Conditional row color
                    fg_color = self.ui.background_main
                    tk.Label(
                        self.cache_scrollable_frame,
                        text=set_value,
                        width=8,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=bg_color,
                        fg=fg_color,
                        relief="solid",
                        borderwidth=0.5
                    ).grid(row=row + 1, column=0, padx=2, pady=1, sticky="nsew")
                    row_data.append(set_value)

                    # Valid column: Initially all cache lines are invalid (0)
                    valid_value = "0"
                    tk.Label(
                        self.cache_scrollable_frame,
                        text=valid_value,
                        width=8,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=bg_color,
                        fg=fg_color,
                        relief="solid",
                        borderwidth=0.5
                    ).grid(row=row + 1, column=1, padx=2, pady=1, sticky="nsew")
                    row_data.append(valid_value)

                    # Tag column: Initially no valid tag ("-")
                    tag_value = "-"
                    tk.Label(
                        self.cache_scrollable_frame,
                        text=tag_value,
                        width=8,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=bg_color,
                        fg=fg_color,
                        relief="solid",
                        borderwidth=0.5
                    ).grid(row=row + 1, column=2, padx=2, pady=1, sticky="nsew")
                    row_data.append(tag_value)

                    # Block data columns: Each cache line will have its block data
                    for col in range(self.block_size):
                        block_value = "-"  # Initially empty data for the block
                        tk.Label(
                            self.cache_scrollable_frame,
                            text=block_value,
                            width=7,
                            height=1,
                            font=("Cascadia Code", 10),
                            bg=bg_color,
                            fg=fg_color,
                            relief="solid",
                            borderwidth=0.5
                        ).grid(row=row + 1, column=3 + col, padx=2, pady=1, sticky="nsew")
                        row_data.append(block_value)

                    # Dirty column: Initially, all cache lines are clean (0)
                    dirty_value = "0"
                    tk.Label(
                        self.cache_scrollable_frame,
                        text=dirty_value,
                        width=6,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=bg_color,
                        fg=fg_color,
                        relief="solid",
                        borderwidth=0.5
                    ).grid(row=row + 1, column=3 + self.block_size, padx=2, pady=1, sticky="nsew")
                    row_data.append(dirty_value)

                    # Append the current row data to the cache_contents list
                    self.cache_contents.append(row_data)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_cache_table(self):
        try:
            if not hasattr(self, "cache_contents"):
                raise AttributeError("Cache contents not initialized. Please create the cache table first.")

            # Clear previous widgets
            for widget in self.cache_scrollable_frame.winfo_children():
                widget.destroy()

            # Create table headers
            headers = ["Set", "Valid", "Tag"] + [f"Byte{i}" for i in range(self.block_size)] + ["Dirty"]
            for col, header in enumerate(headers):
                header_label = tk.Label(
                    self.cache_scrollable_frame,
                    text=header,
                    width=7 if col >= 3 and col < len(headers) - 1 else 6,
                    height=1,
                    font=("Cascadia Code", 10, "bold"),
                    bg=self.ui.background_main,
                    fg=self.ui.font_color_1,
                    relief="solid",
                    borderwidth=1
                )
                header_label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

            # Iterate over the rows in cache_contents
            for row_index, row_data in enumerate(self.cache_contents):
                # Calculate the set index and row color based on the 4-way set-associative structure
                set_idx = row_index // 4  # Each set has 4 lines
                
                # Alternating row colors based on the set index
                bg_color = self.ui.row_color if set_idx % 2 == 1 else self.ui.font_color_1
                fg_color = self.ui.background_main  # Foreground color

                # Iterate over the columns in the row
                for col_index, cell_data in enumerate(row_data):
                    # Determine cell width (wider for block data columns)
                    cell_width = 7 if col_index >= 3 and col_index < len(row_data) - 1 else 6

                    # Create cell labels
                    cell_label = tk.Label(
                        self.cache_scrollable_frame,
                        text=str(cell_data),
                        width=cell_width,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=bg_color,  # Background color from alternating logic
                        fg=fg_color,  # Foreground color
                        relief="solid",
                        borderwidth=0.5
                    )
                    cell_label.grid(row=row_index + 1, column=col_index, padx=2, pady=1, sticky="nsew")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def color_cache_row(self, row, bg_color, fg_color):
        try:
            for widget in self.cache_scrollable_frame.winfo_children():
                grid_info = widget.grid_info()
                widget_row = int(grid_info['row'])  
                if widget_row == row + 1:  
                    widget.config(bg=bg_color, fg=fg_color)  # Apply the colors
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while coloring the cache row: {e}")

    def color_cache_block(self, row, bg_color, fg_color):
        try:
            offset_value = int(self.offset)  
            for widget in self.cache_scrollable_frame.winfo_children():
                grid_info = widget.grid_info()
                widget_row = int(grid_info['row'])  # Convert row to int
                widget_col = int(grid_info['column'])  # Convert column to int
                
                # Check if the row matches and if the column matches (offset + 3)
                if widget_row == (row + 1) and widget_col == (offset_value + 3):
                    widget.config(bg=bg_color, fg=fg_color)  # Apply the colors
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while coloring the cache block: {e}")

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
#---------------------------------------------------------------------------------------------------------------------
  # Load = Read. Retrieves data from memory/cache.
        
    def load_instruction(self, binary_number,addr):
        print("Load :" + str(binary_number))
        self.update_tio(binary_number)
        self.tio_label.config(text="Instruction Breakdown for "+str(addr), fg=self.ui.font_color_1)
        self.ui.window.after(2000, self.check_cache_hit_or_miss_load)

    def check_cache_hit_or_miss_load(self):
        try:
            # Calculate set index and offset
            cache_set_index = int(self.index, 2)  # Convert index binary to integer
            offset_value = int(self.offset, 2)   # Convert offset binary to integer

            # Validate set index and offset
            if cache_set_index >= self.num_sets:
                raise IndexError(f"Cache set index {cache_set_index} is out of range for {self.num_sets} sets.")
            if offset_value >= self.block_size:
                raise ValueError(f"Offset value {offset_value} is out of range for block size {self.block_size}.")

            # Access the four cache lines for the set (4-way associative cache)
            set_start_index = cache_set_index * 4  # The starting index for the set in cache_contents
            set_lines = self.cache_contents[set_start_index:set_start_index + 4]  # Get the 4 cache lines in the set

            # Check all 4 lines for a cache hit
            is_hit = False
            hit_index = None
            for line_index, line in enumerate(set_lines):
                valid_bit = line[1]  # Valid bit
                tag = line[2]       # Tag

                if valid_bit == "1" and self.tag == tag:
                    # Cache hit
                    is_hit = True
                    hit_index = line_index
                    hit_line = line_index
                    break

            if is_hit:
                print("Cache hit")
                if self.replacement_policy == "LRU":
                    self.replacement_array[cache_set_index].remove(hit_line)
                    self.replacement_array[cache_set_index].append(hit_line)
                    
                    print(f"LRU update: {hit_line} is now most recently used")
                    print(f"Replacement Array: {list(self.replacement_array[cache_set_index])}")

                self.cache_title_label.config(text="Cache Hit", fg=self.ui.font_color_1)
                # Highlight the row of the cache line that caused the hit
                self.color_cache_row(set_start_index + line_index, self.ui.color_pink, self.ui.font_color_1)
                data = line[3 + offset_value]  # Retrieve data from the correct byte offset
                # Show the data (simulate the color change for the cache block)
                self.ui.window.after(2000, self.color_block_hit, set_start_index + line_index, None, data)
            else:
                # Cache miss
                replacement_index = self.find_replacement_index(cache_set_index)
                print("Cache miss")
                self.cache_title_label.config(text="Cache Miss", fg=self.ui.font_color_1)
                # Clear all rows in the set
                replacement_line = set_start_index + replacement_index
                
                for line_index in range(4):  # Clear all 4 lines in the set
                    self.color_cache_row(set_start_index + line_index, self.ui.background_main, self.ui.font_color_1)
                # Simulate loading data from main memory
                self.ui.window.after(2000, self.load_data_from_main_memory, replacement_line, offset_value,0)

        except Exception as e:
            print(f"Error in check_cache_hit_or_miss_load: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def find_replacement_index(self,cache_set_index):
        try:
            if self.replacement_policy == "LRU":
                least_recently_used = self.replacement_array[cache_set_index].popleft()  # Correct usage
                self.replacement_array[cache_set_index].append(least_recently_used)
                print(f"LRU replacement: Replacing index {least_recently_used}")
                print(f"Replacement Array: {list(self.replacement_array[cache_set_index])}")

                return least_recently_used

            elif self.replacement_policy == "FIFO":
                first_in = self.replacement_array[cache_set_index].popleft()  # Correct usage
                self.replacement_array[cache_set_index].append(first_in)
                print(f"FIFO replacement: Replacing index {first_in}")
                print(f"Replacement Array: {list(self.replacement_array[cache_set_index])}")

                return first_in

            elif self.replacement_policy == "Random":
                random_index = random.choice(range(4))
                print(f"Random replacement: Replacing index {random_index}")
                return random_index

            else:
                messagebox.showerror("Error", "Invalid replacement policy selected.")
                raise ValueError("Invalid replacement policy")

        except Exception as e:
            print(f"Error in find_replacement_index: {e}")
            messagebox.showerror("Error", f"An error occurred in find_replacement_index: {e}")
            return None

 
    def color_block_hit(self,cache_index,memory_row_index,data):
        self.color_cache_block(cache_index,  self.ui.background_main  ,self.ui.font_color_1 )
        self.cache_title_label.config(text="Data : "+data, fg=self.ui.font_color_1)
        print("Data : "+data)
        self.ui.window.after(4000, self.reset_colors,cache_index,memory_row_index)

    def color_block_miss(self,cache_index,memory_row_index,data):
        self.color_cache_block(cache_index,  self.ui.color_pink  ,self.ui.font_color_1 )
        self.cache_title_label.config(text="Data : "+data, fg=self.ui.font_color_1)
        print("Data : "+data)
        self.ui.window.after(4000, self.reset_colors,cache_index,memory_row_index)

    def reset_colors(self,cache_index,memory_row_index):
        if cache_index is not None:
                set_idx = cache_index //  4
                bg_color = self.ui.row_color if set_idx % 2 == 1 else self.ui.font_color_1
                fg_color = self.ui.background_main  # Foreground color
                self.color_cache_row(cache_index, bg_color,fg_color)
        self.color_main_memory_row(memory_row_index ,self.ui.font_color_1,self.ui.color_pink  )
        self.cache_title_label.config(text="Cache Memory ", fg=self.ui.font_color_1)
        self.tio_label.config(text="Instruction Breakdown", fg=self.ui.font_color_1)
        binary_zero = bin(0)[2:]
        self.update_tio(binary_zero)

    def load_data_from_main_memory(self,replacement_line_index, offset_value, instr):
        try:
            self.cache_title_label.config(text="Cache Miss: Load data from main memory", fg=self.ui.font_color_1)
            
            # Construct the memory row index
            memory_row_index = int(self.tag + self.index, 2)

            # Validate memory row index
            if memory_row_index >= len(self.main_contents):
                print(f"Error: Memory row index {memory_row_index} exceeds main memory size.")
                return

            # Get the memory row data
            memory_row = self.main_contents[memory_row_index]

            # Check if the memory row has sufficient data for the block
            if len(memory_row) <= offset_value:
                print(f"Error: Memory row {memory_row_index} does not contain enough data.")
                return
            
            # Check if the block has been modified and needs to be written back to memory
            if self.write_hit_policy == "write-back":
                # If the cache block is dirty (dirty bit is 1), write back to main memory
                if self.cache_contents[replacement_line_index][-1] == "1" and self.cache_contents[replacement_line_index][1]  == "1":
                    print(f"Write-back: Writing dirty block {replacement_line_index} back to main memory.")
                    # Write the dirty block back to main memory
                    # Extract the new tag and index from the cache contents
                    new_index = self.cache_contents[replacement_line_index][0]  # Cache's index field
                    new_tag = self.cache_contents[replacement_line_index][2]  # Cache's tag field
                    new_memory_row_index = int(new_tag + new_index, 2) 
                    for block in range(self.block_size):
                       self.main_contents[new_memory_row_index][block] = self.cache_contents[replacement_line_index][3 + block]
                    self.update_main_memory_table()   
                    print(f"Data from cache index {replacement_line_index} written back to memory row {new_memory_row_index}.")

            # Proceed with loading the new data into the cache
            cache_line = self.cache_contents[replacement_line_index]
            cache_line[1] = "1"  # Set the valid bit to "1" (mark as valid)
            cache_line[2] = self.tag  # Set the tag
            cache_line[-1] = "0"  # Set the dirty bit to "0" (clean line)

            # Load data from memory into the cache line
            for block_index in range(self.block_size):
                if block_index < len(memory_row):
                    cache_line[3 + block_index] = memory_row[block_index]

            # Update the cache table to reflect the new data
            self.update_cache_table()

            # Highlight the cache line that was updated
            self.color_cache_row(replacement_line_index, self.ui.background_main, self.ui.font_color_1)
            
            # Highlight the corresponding row in the main memory
            self.color_main_memory_row(memory_row_index, self.ui.color_pink, self.ui.font_color_1)

            # Scroll the main memory view to the updated row
            for widget in self.main_scrollable_frame.winfo_children():
                grid_info = widget.grid_info()
                row = int(grid_info['row'])
                if row == memory_row_index + 1:
                    row_height = widget.winfo_height()
                    row_y_position = row * row_height
                    self.main_canvas.yview_moveto(row_y_position / self.main_canvas.bbox("all")[3])

            # Show the loaded data from the cache line
            data = str(cache_line[3 + offset_value])
            print(f"Loaded data from main memory block {memory_row_index} into cache line {replacement_line_index}.")
            if instr == 0:
                    self.ui.window.after(4000, self.color_block_miss, replacement_line_index, memory_row_index, data)
            else:
                    self.cache_contents[replacement_line_index][-1] = "1"
                    self.cache_contents[replacement_line_index][3 + offset_value] = self.data_byte
                    self.update_cache_table()
                    self.color_cache_row(replacement_line_index, self.ui.background_main, self.ui.font_color_1)
                    self.ui.window.after(4000, self.color_block_miss,replacement_line_index,memory_row_index,self.data_byte)
            
        except Exception as e:
            print(f"Error in load_data_from_main_memory: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

#---------------------------------------------------------------------------------------------------------------------
   # Store = Write. Saves data to memory/cache.
    def store_instruction(self, address_binary, data_byte, addr):
        self.data_byte = data_byte
        print("Store at address : " + str(address_binary) + "   data : " + self.data_byte)
        self.update_tio(address_binary)
        self.tio_label.config(text="Instruction Breakdown for " + str(addr), fg=self.ui.font_color_1)
        self.ui.window.after(2000, self.check_cache_hit_or_miss_store)

  
    def check_cache_hit_or_miss_store(self):
        try:
            # Calculate set index and offset
            cache_set_index = int(self.index, 2)  # Convert index binary to integer
            offset_value = int(self.offset, 2)   # Convert offset binary to integer

            # Validate set index and offset
            if cache_set_index >= self.num_sets:
                raise IndexError(f"Cache set index {cache_set_index} is out of range for {self.num_sets} sets.")
            if offset_value >= self.block_size:
                raise ValueError(f"Offset value {offset_value} is out of range for block size {self.block_size}.")

            # Access the four cache lines for the set (4-way set associative)
            set_start_index = cache_set_index * 4  # First line in the set
            set_lines = [
                self.cache_contents[set_start_index],
                self.cache_contents[set_start_index + 1],
                self.cache_contents[set_start_index + 2],
                self.cache_contents[set_start_index + 3]
            ]

            # Check all lines for a cache hit
            is_hit = False
            hit_index = None
            for line_index, line in enumerate(set_lines):
                valid_bit = line[1]  # Valid bit
                tag = line[2]       # Tag

                if valid_bit == "1" and self.tag == tag:
                    # Cache hit
                    is_hit = True
                    hit_index = set_start_index + line_index
                    hit_line = line_index
                    break

            if is_hit:
                # Cache hit: Write data to cache
                print("Cache hit")
                print (cache_set_index)
                self.cache_contents[hit_index][3 + offset_value] = self.data_byte  # Write data to cache
                self.cache_title_label.config(text="Cache Hit", fg=self.ui.font_color_1)
                if self.replacement_policy == "LRU":
                    self.replacement_array[cache_set_index].remove(hit_line)
                    self.replacement_array[cache_set_index].append(hit_line)
                    
                    print(f"LRU update: {hit_line} is now most recently used")
                    print(f"Replacement Array: {list(self.replacement_array[cache_set_index])}")

                if self.write_hit_policy == "write-back":
                    # Write-back: Write to cache + Mark dirty bit
                    self.cache_contents[hit_index][-1] = "1"  # Set dirty bit
                    print("Write-back: Data written to cache and block marked dirty.")
                else:
                    # Write-through: Update both cache and main memory
                    print("Write-through: Data written to cache and main memory.")
                    self.update_main_memory(offset_value, self.data_byte)

                self.update_cache_table()
                self.color_cache_row(hit_index, self.ui.color_pink, self.ui.font_color_1)
                self.ui.window.after(2000, self.color_block_hit, hit_index, None, self.data_byte)

            else:
                # Cache miss
                print("Cache miss")
                self.cache_title_label.config(text="Cache Miss", fg=self.ui.font_color_1)
                
                if self.write_miss_policy == "write-allocate":
                    # Write-allocate: Load block into cache and write data
                    print("Write-allocate: Loading block into cache and writing data.")
                    replacement_index = self.find_replacement_index(cache_set_index)
                    replacement_line = set_start_index + replacement_index
                    self.color_cache_row(replacement_index, self.ui.background_main, self.ui.font_color_1)
                    self.ui.window.after(2000, self.load_data_from_main_memory, replacement_line, offset_value, 1)
                else:
                    # No-write-allocate: Write directly to main memory
                    print("No-write-allocate: Writing data directly to main memory.")
                    self.ui.window.after(2000, self.no_write_allocate, offset_value, self.data_byte)

        except Exception as e:
            print(f"Error in check_cache_hit_or_miss_store: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_main_memory(self, offset_value, data_byte):
        try:
            # Update the main memory contents
            memory_row_index = int(self.tag + self.index, 2)  # Calculate memory row index from the tag and index
            self.main_contents[memory_row_index][offset_value] = data_byte

            print(f"Main memory updated at block {memory_row_index}, word {offset_value} with data: {data_byte}.")
            self.update_main_memory_table()
            self.color_main_memory_row(memory_row_index, self.ui.color_pink, self.ui.font_color_1)

            # Scroll to the updated block in main memory
            for widget in self.main_scrollable_frame.winfo_children():
                grid_info = widget.grid_info()
                row = int(grid_info['row'])

                if row == memory_row_index + 1:  # +1 for 1-based row indexing
                    row_height = widget.winfo_height()
                    total_canvas_height = self.main_canvas.bbox("all")[3]
                    row_y_position = row * row_height

                    scroll_position = row_y_position / total_canvas_height
                    self.main_canvas.yview_moveto(scroll_position)

        except Exception as e:
            print(f"Error in update_main_memory: {e}")
            messagebox.showerror("Error", f"An error occurred while updating main memory: {e}")

    def no_write_allocate(self, offset_value, data_byte):
        try:
            # Calculate memory row index from tag and index
            memory_row_index = int(self.tag + self.index, 2)
            
            # Validate memory row index
            if memory_row_index >= len(self.main_contents):
                raise IndexError(f"Memory row index {memory_row_index} exceeds main memory size.")

            # Update the specific byte in main memory
            self.main_contents[memory_row_index][offset_value] = data_byte
            print(f"No-Write-Allocate: Data written in main memory at row {memory_row_index}, offset {offset_value}")
            
            # Update the main memory table in the UI
            self.update_main_memory_table()
            self.color_main_memory_row(memory_row_index, self.ui.color_pink, self.ui.font_color_1)
            
            # Update the UI cache title label
            self.cache_title_label.config(
                text=f"No-Write-Allocate: Data written to main memory at row {memory_row_index}, offset {offset_value}",
                fg=self.ui.font_color_1
            )
            
            # Scroll to the updated block in main memory for user visibility
            for widget in self.main_scrollable_frame.winfo_children():
                grid_info = widget.grid_info()
                row = int(grid_info['row'])
                
                if row == memory_row_index + 1:  # +1 for 1-based row indexing
                    row_height = widget.winfo_height()
                    total_canvas_height = self.main_canvas.bbox("all")[3]
                    row_y_position = row * row_height

                    scroll_position = row_y_position / total_canvas_height
                    self.main_canvas.yview_moveto(scroll_position)
            
            # Reset colors after a delay
            self.ui.window.after(4000, self.reset_colors, None, memory_row_index)

        except Exception as e:
            print(f"Error in no_write_allocate: {e}")
            messagebox.showerror("Error", f"An error occurred in no_write_allocate: {e}")

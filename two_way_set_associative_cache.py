import tkinter as tk
from tkinter import ttk, messagebox

class Two_way_set_associative_cache:
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
        # Declare the variables for 2-way set-associative cache simulation
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
    def two_way_set_associative(self):
        if not self.validate():
            return
        
        self.num_blocks = self.cache_size // self.block_size
        self.num_sets = self.num_blocks // 2  # 2-way set-associative cache (2 cache lines per set)
        
        # Number of bits for block offset
        self.block_offset_bits = (self.block_size - 1).bit_length()
        
        # Number of bits for index (for the number of sets)
        self.index_bits = (self.num_sets - 1).bit_length()
        
        # Number of bits for tag
        self.tag_bits = self.address_width - (self.index_bits + self.block_offset_bits)

        print(f":::::::::::::::::::::::::::::::::::")
        print(f"2-Way Set-Associative Cache Simulation:")
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
        
        self.tio_label = tk.Label(
            self.ui.output_container,
            text="Instruction Breakdown",
            font=("Cascadia Code", 16, "bold"),
            bg=self.ui.background_container,
            fg=self.ui.font_color_1
        )
        self.tio_label.grid(row=0, column=0, columnspan=3, padx=5, pady=(10, 5), sticky="W")
        
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
        self.create_cache_table()
    #---------------------------------------------------------------------------------------------------------------------
    def update_tio(self, binary_number):
        binary_zero = bin(0)[2:].zfill(self.address_width)
        binary_number = binary_number.zfill(self.address_width)
        self.tag = binary_number[:self.tag_bits]
        self.index = binary_number[self.tag_bits:self.tag_bits + self.index_bits]
        self.offset = binary_number[self.tag_bits + self.index_bits:]
        if binary_number != binary_zero:
            print(f"Tag: {self.tag}")
            print(f"Index: {self.index}")
            print(f"Offset: {self.offset}")
        
        for widget in self.ui.output_container.winfo_children():
            if int(widget.grid_info()['row']) == 2:
                widget.destroy()

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
            for widget in self.ui.cache_memory_container.winfo_children():
                widget.destroy()

            self.cache_title_label = tk.Label(self.ui.cache_memory_container, text="Cache Memory", font=("Cascadia Code", 16, "bold"), bg=self.ui.background_container, fg=self.ui.font_color_1)
            self.cache_title_label.pack(side="top", anchor="nw", pady=(10, 5), padx=5)
            self.cache_contents.clear()

            # Create a frame for the table
            frame = tk.Frame(self.ui.cache_memory_container)
            frame.pack(fill="both", expand=True)

            # Set up canvas and scrollbars
            canvas = tk.Canvas(frame, height=210, width=280)
            vertical_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            self.cache_scrollable_frame = ttk.Frame(canvas)

            self.cache_scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            # Create the scrollable window and set the vertical scrollbar
            canvas.create_window((0, 0), window=self.cache_scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=vertical_scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            vertical_scrollbar.pack(side="right", fill="y")

            # Create the table headers (move "Index" to the first position)
            headers = ["Index", "Set", "Valid", "Tag"] + [f"Byte{i}" for i in range(self.block_size)] + ["Dirty"]
            for col, header in enumerate(headers):
                header_label = tk.Label(self.cache_scrollable_frame, text=header, width=6, height=1, font=("Cascadia Code", 10, "bold"),
                                        bg=self.ui.background_main, fg=self.ui.font_color_1, relief="solid", borderwidth=1)
                header_label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

            # Create the table rows
            for set_idx in range(self.num_sets):  # Iterate over the sets
                for line_idx in range(2):  # Each set has 2 cache lines
                    row = set_idx * 2 + line_idx  # Row in the table (representing the cache line)

                    # List to hold row content
                    row_data = []

                    # Determine if the set index is even, and set color if so
                    bg_color = self.ui.row_color if set_idx % 2 == 1 else self.ui.font_color_1
                    fg_color = self.ui.background_main

                    # Apply color to the row if set_idx is even
                    if set_idx % 2 == 0:
                        self.color_cache_row(row, bg_color, fg_color)

                    # Index column: Show the index value for the set
                    index_value = f"{row}"  # Index within the set (e.g., 0 or 1 for 2-way cache)
                    tk.Label(
                        self.cache_scrollable_frame,
                        text=index_value,
                        width=8,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=bg_color,
                        fg=fg_color,
                        relief="solid",
                        borderwidth=0.5
                    ).grid(row=row + 1, column=0, padx=2, pady=1, sticky="nsew")
                    row_data.append(index_value)

                    # Set column: Show which set this cache line belongs to
                    set_value = f"{set_idx}"
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
                    ).grid(row=row + 1, column=1, padx=2, pady=1, sticky="nsew")
                    row_data.append(set_value)

                    # Valid column
                    valid_value = "0"  # Initially, all lines are invalid
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
                    ).grid(row=row + 1, column=2, padx=2, pady=1, sticky="nsew")
                    row_data.append(valid_value)

                    # Tag column
                    tag_value = "-"  # Initially, all cache lines have no valid tag
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
                    ).grid(row=row + 1, column=3, padx=2, pady=1, sticky="nsew")
                    row_data.append(tag_value)

                    # Block data columns
                    for col in range(self.block_size):
                        block_value = "-"  # Initial empty block data
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
                        ).grid(row=row + 1, column=4 + col, padx=2, pady=1, sticky="nsew")
                        row_data.append(block_value)

                    # Dirty column
                    dirty_value = "0"  # Initially, all cache lines are clean
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
                    ).grid(row=row + 1, column=4 + self.block_size, padx=2, pady=1, sticky="nsew")
                    row_data.append(dirty_value)

                    # Append the row to cache_contents
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
            headers = ["Index", "Valid", "Tag"] + [f"Byte{i}" for i in range(self.block_size)] + ["Dirty"]
            for col, header in enumerate(headers):
                header_label = tk.Label(
                    self.cache_scrollable_frame,
                    text=header,
                    width=6,
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
                set_idx = row_index // 2  # Calculate the set index
                bg_color = self.ui.row_color if set_idx % 2 == 1 else self.ui.font_color_1  # Conditional background color
                fg_color = self.ui.background_main  # Foreground color

                # Iterate over the columns in the row
                for col_index, cell_data in enumerate(row_data):
                    # Calculate the cell width based on column index (data columns should be wider)
                    cell_width = 7 if col_index >= 3 and col_index < len(row_data) - 1 else 6

                    # Create the cell label with the appropriate background and foreground colors
                    cell_label = tk.Label(
                        self.cache_scrollable_frame,
                        text=str(cell_data),  
                        width=cell_width,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=bg_color,
                        fg=fg_color,
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

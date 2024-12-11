import tkinter as tk
import random
from collections import deque
from tkinter import ttk, messagebox
class Fully_associative_cache:
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
        

        self.replacement_array = deque(range(self.cache_size // self.block_size))
        self.num_blocks = 0
        self.block_offset_bits = 0
        self.index_bits = 0
        self.tag_bits = 0
        self.tag = '0'
        self.index = '0'
        self.offset = '0'
        self.data_byte= ""

#---------------------------------------------------------------------------------------------------------------------
    def fully_associative(self):
        if not self.validate():
            return 
        self.num_blocks = self.cache_size // self.block_size
        self.block_offset_bits = (self.block_size - 1).bit_length()  # log2(block_size)
        self.tag_bits = self.address_width -  self.block_offset_bits
        
        print(f"Fully-Associative Cache Simulation:")
        print(f"Cache size: {self.cache_size}")
        print(f"Address width: {self.address_width}")
        print(f"Block size: {self.block_size}")
        print(f"Number of blocks: {self.num_blocks}")
        print(f"Tag bits: {self.tag_bits}")
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

        headers = ["Tag", "Offset"]
        for col, header in enumerate(headers):
            header_label = tk.Label(
                self.ui.output_container,
                text=header,
                width=19,
                height=2,
                font=("Cascadia Code", 14, "bold"),
                bg=self.ui.background_main,
                fg=self.ui.font_color_1,
                relief="solid",
                borderwidth=1
            )
            header_label.grid(row=1, column=col, padx=5, pady=7, sticky="nsew")

        zeros = ['0' * self.tag_bits, '0' * self.block_offset_bits]
        for col, value in enumerate(zeros):
            row_label = tk.Label(
                self.ui.output_container,
                text=value,
                width=19,
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
        if binary_number != binary_zero :
            print(f"Tag: {self.tag}")
            print(f"Offset: {self.offset}")
        for widget in self.ui.output_container.winfo_children():
            if int(widget.grid_info()['row']) == 2:
                widget.destroy()

        values = [self.tag, self.offset]
        for col, value in enumerate(values):
            row_label = tk.Label(
                self.ui.output_container,
                text=value,
                width=19,
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
            # Ensure the table exists
            if not hasattr(self, "main_contents"):
                raise AttributeError("Main memory contents not initialized. Please create the main memory table first.")

            # Clear existing widgets in the scrollable frame
            for widget in self.main_scrollable_frame.winfo_children():
                widget.destroy()

            # Recreate the table using updated contents
            for block_index, block_data in enumerate(self.main_contents):
                for word_index, word_data in enumerate(block_data):
                    word_label = ttk.Label(
                        self.main_scrollable_frame,
                        text=str(word_data),  # Convert to string for display
                        width=10,
                        anchor="center"
                    )
                    word_label.grid(
                        row=(block_index * 2) + 1, column=word_index, padx=5, pady=2, sticky="nsew"
                    )
                    
                    # If a search index is provided and matches the current block, color the row
                    if search_index is not None and block_index == search_index:
                        word_label.config(bg="yellow", fg="black")  # Change the background and text color for the searched row
                    else:
                        word_label.config(bg=self.ui.background_main, fg=self.ui.font_color_1)  # Reset to default colors

        except Exception as e:
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

            # Create the table headers
            headers = ["Index", "Valid", "Tag"] + [f"Byte{i}" for i in range(self.block_size)] + ["Dirty"]
            for col, header in enumerate(headers):
                header_label = tk.Label(self.cache_scrollable_frame, text=header, width=6, height=1, font=("Cascadia Code", 10, "bold"),
                                        bg=self.ui.background_main, fg=self.ui.font_color_1, relief="solid", borderwidth=1)
                header_label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")

            # Create the table rows
            for row in range(self.num_blocks):
                # List to hold row content
                row_data = []

                # Index column
                index_value = f"{row}"
                tk.Label(
                    self.cache_scrollable_frame,
                    text=index_value,
                    width=8,
                    height=1,
                    font=("Cascadia Code", 10),
                    bg=self.ui.font_color_1,
                    fg=self.ui.background_main,
                    relief="solid",
                    borderwidth=0.5
                ).grid(row=row + 1, column=0, padx=2, pady=1, sticky="nsew")
                row_data.append(index_value)

                # Valid column
                valid_value = "0"
                tk.Label(
                    self.cache_scrollable_frame,
                    text=valid_value,
                    width=8,
                    height=1,
                    font=("Cascadia Code", 10),
                    bg=self.ui.font_color_1,
                    fg=self.ui.background_main,
                    relief="solid",
                    borderwidth=0.5
                ).grid(row=row + 1, column=1, padx=2, pady=1, sticky="nsew")
                row_data.append(valid_value)

                # Tag column
                tag_value = "-"
                tk.Label(
                    self.cache_scrollable_frame,
                    text=tag_value,
                    width=8,
                    height=1,
                    font=("Cascadia Code", 10),
                    bg=self.ui.font_color_1,
                    fg=self.ui.background_main,
                    relief="solid",
                    borderwidth=0.5
                ).grid(row=row + 1, column=2, padx=2, pady=1, sticky="nsew")
                row_data.append(tag_value)

                # Block data columns
                for col in range(self.block_size):
                    block_value = "-"
                    tk.Label(
                        self.cache_scrollable_frame,
                        text=block_value,
                        width=7,
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=self.ui.font_color_1,
                        fg=self.ui.background_main,
                        relief="solid",
                        borderwidth=0.5
                    ).grid(row=row + 1, column=3 + col, padx=2, pady=1, sticky="nsew")
                    row_data.append(block_value)

                # Dirty column
                dirty_value = "0"
                tk.Label(
                    self.cache_scrollable_frame,
                    text=dirty_value,
                    width=6,
                    height=1,
                    font=("Cascadia Code", 10),
                    bg=self.ui.font_color_1,
                    fg=self.ui.background_main,
                    relief="solid",
                    borderwidth=0.5
                ).grid(row=row + 1, column=3 + self.block_size, padx=2, pady=1, sticky="nsew")
                row_data.append(dirty_value)

                # Append the row to cache_contents
                self.cache_contents.append(row_data)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_cache_table(self):
        try:
            if not hasattr(self, "cache_contents"):
                raise AttributeError("Cache contents not initialized. Please create the cache table first.")

            for widget in self.cache_scrollable_frame.winfo_children():
                widget.destroy()

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

            for row_index, row_data in enumerate(self.cache_contents):
                for col_index, cell_data in enumerate(row_data):
                    cell_label = tk.Label(
                        self.cache_scrollable_frame,
                        text=str(cell_data),  
                        width=7 if col_index >= 3 and col_index < len(row_data) - 1 else 6, 
                        height=1,
                        font=("Cascadia Code", 10),
                        bg=self.ui.font_color_1,
                        fg=self.ui.background_main,
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
 #LOAD - read
    def load_instruction(self, binary_number,addr):
        print("Load :" + str(binary_number))
        self.update_tio(binary_number)
        self.tio_label.config(text="Instruction Breakdown for "+str(addr), fg=self.ui.font_color_1)
        self.ui.window.after(2000, self.check_cache_hit_or_miss_load)

    def check_cache_hit_or_miss_load(self):
        try:
            offset_value = int(self.offset, 2)  
            tag = self.tag  

            is_hit = False
            hit_index = None
            for row_index, row in enumerate(self.cache_contents):
                valid_bit = row[1]  
                cache_tag = row[2]  

                if valid_bit == "1" and cache_tag == tag:
                    is_hit = True
                    hit_index = row_index
                    break

            if is_hit:
                # Cache hit
                data = self.cache_contents[hit_index][3 + offset_value]
                print("Cache Hit")
                if self.replacement_policy == "LRU":
                    if hit_index in self.replacement_array:
                        self.replacement_array.remove(hit_index)
                    self.replacement_array.append(hit_index)
                    print(f"LRU update: {hit_index} is now most recently used")
                    print(f"Replacement Array: {list(self.replacement_array)}")

                self.cache_title_label.config(text="Cache Hit", fg=self.ui.font_color_1)
                self.color_cache_row(hit_index, self.ui.color_pink, self.ui.font_color_1)
                self.ui.window.after(2000, self.color_block_hit, hit_index, None, data)
            else:
                # Cache miss
                replacement_index = self.find_replacement_index()
                print("Cache Miss")
                self.cache_title_label.config(text="Cache Miss - replacement index: " + str(replacement_index), fg=self.ui.font_color_1)
                self.color_cache_row(replacement_index, self.ui.background_main, self.ui.font_color_1)
                self.ui.window.after(2000, self.load_data_from_main_memory, tag, offset_value, replacement_index,0)

        except Exception as e:
            print(f"Error in check_cache_hit_or_miss_load: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_data_from_main_memory(self, tag, offset_value, replacement_index,instr):
        try:
            # Calculate the memory row index from the tag
            memory_row_index = int(tag, 2)
            self.cache_title_label.config(text="Cache Miss : Load data from main memory", fg=self.ui.font_color_1)
        
            if memory_row_index >= len(self.main_contents):
                print(f"Error: Memory row index {memory_row_index} exceeds main memory size.")
                return

            # Fetch the memory row
            memory_row = self.main_contents[memory_row_index]
            if len(memory_row) <= offset_value:
                print(f"Error: Memory row {memory_row_index} does not contain enough data.")
                return
            
            # Update cache contents
            self.cache_contents[replacement_index][1] = "1"  # Set valid bit
            self.cache_contents[replacement_index][2] = tag  # Set tag

            for block in range(self.block_size):
                if block < len(memory_row): 
                    self.cache_contents[replacement_index][3 + block] = memory_row[block]
                else:
                    print(f"Error: Block {block} is out of range for memory row {memory_row_index}")

            # Update UI
            self.update_cache_table()
            self.color_cache_row(replacement_index, self.ui.background_main, self.ui.font_color_1)
            self.color_main_memory_row(memory_row_index, self.ui.color_pink, self.ui.font_color_1)

            # Scroll to the corresponding main memory row
            for widget in self.main_scrollable_frame.winfo_children():
                grid_info = widget.grid_info()
                row = int(grid_info['row'])  
                if row == memory_row_index + 1: 
                    row_height = widget.winfo_height() 
                    row_y_position = row * row_height  
                    self.main_canvas.yview_moveto(row_y_position / self.main_canvas.bbox("all")[3]) 
            
            # Extract data from the fetched memory row
            data = str(self.cache_contents[replacement_index][3 + offset_value])
            print(f"Loaded data from main memory row {memory_row_index} to cache index {replacement_index}.")

            # After loading data, highlight the row and show in UI
            if instr == 0:
                self.ui.window.after(4000, self.color_block_miss,replacement_index,memory_row_index,data)
            else:
                self.cache_contents[replacement_index][3 + offset_value] = self.data_byte
                self.update_cache_table()
                self.color_cache_row(replacement_index, self.ui.background_main, self.ui.font_color_1)
            
                self.ui.window.after(4000, self.color_block_miss,replacement_index,memory_row_index,self.data_byte)

        except Exception as e:
            print(f"Error in load_data_from_main_memory: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def find_replacement_index(self):
        try:
            if self.replacement_policy == "LRU":
                least_recently_used = self.replacement_array.popleft()  # Correct usage
                self.replacement_array.append(least_recently_used)
                print(f"LRU replacement: Replacing index {least_recently_used}")
                print(f"Replacement Array: {list(self.replacement_array)}")

                return least_recently_used

            elif self.replacement_policy == "FIFO":
                first_in = self.replacement_array.popleft()  # Correct usage
                self.replacement_array.append(first_in)
                print(f"FIFO replacement: Replacing index {first_in}")
                print(f"Replacement Array: {list(self.replacement_array)}")

                return first_in

            elif self.replacement_policy == "Random":
                random_index = random.choice(range(len(self.cache_contents)))
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
        if(cache_index!=None):
            self.color_cache_row(cache_index,self.ui.font_color_1  ,self.ui.background_main  )
        self.color_main_memory_row(memory_row_index ,self.ui.font_color_1,self.ui.color_pink  )
        self.cache_title_label.config(text="Cache Memory ", fg=self.ui.font_color_1)
        self.tio_label.config(text="Instruction Breakdown", fg=self.ui.font_color_1)
        binary_zero = bin(0)[2:]
        self.update_tio(binary_zero)

#---------------------------------------------------------------------------------------------------------------------
    # Store = Write. Saves data to memory/cache.

    def store_instruction(self, address_binary,data_byte,addr):
        self.data_byte=data_byte
        print("Store at address : " + str(address_binary) + "   data : " +self.data_byte)
        self.update_tio(address_binary)
        self.tio_label.config(text="Instruction Breakdown for "+str(addr), fg=self.ui.font_color_1)
        self.ui.window.after(2000, self.check_cache_hit_or_miss_store)

    def check_cache_hit_or_miss_store(self):
        try:
            offset_value = int(self.offset, 2)  # Convert the offset to an integer
            tag = self.tag  # Get the tag

            is_hit = False
            hit_index = None

            # Search for a cache hit by comparing the tag and valid bit
            for row_index, row in enumerate(self.cache_contents):
                valid_bit = row[1]  # Valid bit
                cache_tag = row[2]  # Tag
                if valid_bit == "1" and cache_tag == tag:
                    is_hit = True
                    hit_index = row_index
                    break  # Exit the loop once a hit is found

            if is_hit:
                # Cache hit: Write data to cache
                self.cache_title_label.config(text="Cache Hit", fg=self.ui.font_color_1)
                self.cache_contents[hit_index][3 + offset_value] = self.data_byte  # Write data to the cache
                
                if self.write_hit_policy == "write-back":
                    # Write-back: Update cache only, set dirty bit
                    print("Write-back: Writing data to cache and marking block dirty.")
                    self.cache_contents[hit_index][3 + self.block_size] = "1"  # Set dirty bit
                    self.update_cache_table()
                    self.color_cache_row(hit_index, self.ui.color_pink, self.ui.font_color_1)
                    self.ui.window.after(2000, self.color_block_hit, hit_index, None, self.data_byte)
                else:
                    # Write-through: Update both cache and main memory
                    print("Write-through: Writing data to cache and main memory.")
                    self.update_main_memory(offset_value, self.data_byte)
                    self.update_cache_table()
                    self.color_cache_row(hit_index, self.ui.color_pink, self.ui.font_color_1)
                    self.ui.window.after(2000, self.color_block_hit, hit_index, None, self.data_byte)

            else:
                # Cache miss: Find the replacement index
                self.cache_title_label.config(text="Cache Miss", fg=self.ui.font_color_1)

                replacement_index = self.find_replacement_index()  # Find the index for replacement

                if self.write_miss_policy == "write-allocate":
                    # Write-Allocate: Load the block into the cache and write the data to the cache
                    print("Write-Allocate: Load the block into the cache and write the data to cache.")
                    # Set the dirty bit for the replacement index
                    self.cache_contents[replacement_index][3 + self.block_size] = "1"  # Set dirty bit
                    self.color_cache_row(replacement_index, self.ui.background_main, self.ui.font_color_1)
                    self.ui.window.after(2000, self.load_data_from_main_memory, tag, offset_value, replacement_index, 1)
                else:
                    # No-Write-Allocate: Write directly to main memory
                    print("No-Write-Allocate: Writing data directly to main memory without loading the block into cache.")
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
        # If it's a No-Write-Allocate miss policy, update the main memory directly.
        memory_row_index = int(self.tag + self.index, 2)  # Calculate memory row index from tag and index
        self.main_contents[memory_row_index][offset_value] = data_byte
        print(f"No-Write-Allocate: Data written directly to main memory at {memory_row_index}, offset {offset_value}")
        self.update_main_memory_table()
        self.color_main_memory_row(memory_row_index, self.ui.color_pink, self.ui.font_color_1)
        self.cache_title_label.config(text="No-Write-Allocate: Data written directly to main memory at {memory_row_index}, offset {offset_value}", fg=self.ui.font_color_1)

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
        
        self.ui.window.after(4000, self.reset_colors,None,memory_row_index)


from replacement_policies import LRUalghorithm,FIFOalgorithm,RANDOMalgorithm
from tkinter import messagebox

class Simulation:
    def __init__(self, ui):
        self.ui = ui
        self.algorithm = None
        self.access_sequence = []
        self.capacity = ui.capacity.get()

        self.frame_labels = []
        self.label_faults = None
        self.label_pages = None

    def run_simulation(self):
        replacement_policy = self.ui.replacement_policy.get()
        self.capacity = self.ui.capacity.get()
        input_sequence = self.ui.input.get()

        try:
            self.access_sequence = list(map(int, input_sequence.split(',')))
        except ValueError:
            messagebox.showerror("Invalid Input", "Input sequence must be comma-separated integers.")
            return

        self.ui.create_frame_labels(self.capacity)

        match replacement_policy:
                case "LRU":
                    self.algorithm = LRUalghorithm(self.capacity)
                case "FIFO":
                    self.algorithm = FIFOalgorithm(self.capacity)
                case "Random":
                    self.algorithm = RANDOMalgorithm(self.capacity)
                case _:
                    messagebox.showerror("Error", "Invalid replacement policy selected.")
                    return

        self.simulation_index = 0
        self.simulate_step()

    def simulate_step(self):
        if self.simulation_index < len(self.access_sequence):
            current_page = self.access_sequence[self.simulation_index]
            self.algorithm.access(current_page)
            cache = self.algorithm.get_cache()
            self.ui.update_canvas(current_page, cache)
            self.simulation_index += 1
            self.ui.window.after(2000, self.simulate_step)  # 2 seconds delay
        else:
            print("Simulation completed.")
            messagebox.showinfo("Simulation Completed", "All pages processed.")

    
    def update_pages_display(self, cache):
        self.label_pages.config(text=f"Used pages: {', '.join(map(str, current_memory))}")
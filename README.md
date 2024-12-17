# 🌟 Cache Memory Simulator 🌟

## 👀 Overview
The Cache Memory Simulator is a graphical user interface (GUI) tool that models the behavior of various cache memory algorithms. Users can adjust cache settings, input memory access sequences, and run simulations to observe how different algorithms—such as Direct-Mapped, Fully Associative, 2-Way Set Associative, and 4-Way Set Associative—manage memory operations, along with handling various replacement policies.

This simulator allows users to visualize cache hits and misses and configure various parameters such as cache size, address width, block size, and more. It is built using Python's `tkinter` library for the user interface and can be extended for educational purposes or performance analysis of cache memory systems.

The Cache Memory Simulator is an interactive graphical user interface (GUI) tool built using Python's tkinter library, designed to model the behavior of various cache memory configurations. It allows users to customize cache parameters, input memory access sequences, and run simulations to observe how different cache mapping techniques—such as Direct-Mapped, Fully Associative, 2-Way Set Associative, and 4-Way Set Associative—manage memory operations. Additionally, the simulator supports a variety of replacement policies to demonstrate their impact on cache performance.

The simulator provides an interactive visualization, enabling users to monitor the dynamic behavior of both the cache and memory in real-time. Users can see how cache configuration choices, like cache size, address width, and block size, influence the system's performance. As users perform actions (such as load or store operations), the interface updates automatically, visually indicating cache hits, misses, and the modification of data in the cache or memory.

This tool supports both load and store operations, and its behavior is governed by the cache hit or miss policies. The simulator’s key functions allow users to better understand the impact of cache management decisions and explore how different configurations can optimize memory access patterns for improved performance.

## ☄️ Features

- **🧑‍💻 User Interface**: Built with `tkinter`, allowing interactive configuration and simulation of cache memory systems.
- **💾Cache Algorithms Supported**:
  - **Direct-Mapped Cache**
  - **Fully Associative Cache**
  - **2-Way Set Associative Cache**
  - **4-Way Set Associative Cache**
- **⚙️Cache Configuration Options**:
  - Cache size
  - Address width
  - Block size
  - Write hit policy
  - Write miss policy
  - Replacement policy
  - Capacity of cache lines
- **.
🧠 Input Types**:
  - Supports LOAD and STORE instructions
  - Hexadecimal and address-data inputs
- **🎨Visual Feedback**:
  - Cache memory states are displayed, indicating cache hits and misses.

## 🔍 Prerequisites

To run this simulator, you'll need:

- Python 3.x installed on your machine
- `tkinter` library (usually included with Python by default)
- No additional dependencies are required for the core functionality.

## 💆‍♀️Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ralucaand03/CacheMemorySimulator.git

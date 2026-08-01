# Multi-Threaded Python Port Scanner

A fast, interactive, and lightweight TCP port scanner written in Python 3. It allows users to scan custom port ranges or target common network services with multi-threaded efficiency.

## Features

- **Interactive Console Menu:** Easily switch between custom port ranges and quick common port scans.
- **Service Name Resolution:** Identifies target services (e.g., SSH, HTTP, MySQL) alongside port numbers.
- **Multi-Threaded Performance:** Powered by `concurrent.futures.ThreadPoolExecutor` for high-speed scanning without resource exhaustion.
- **Error Handling & Resilience:** Robust handling for invalid user inputs, host resolution failures, and graceful exit routines.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MuhammadAhmadd1/port-scanner.git](https://github.com/MuhammadAhmadd1/port-scanner.git)
   cd port-scanner

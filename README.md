# gpudatacollector

This project is designed to collect GPU data from all NVIDIA workstations. It is structured into several main parts to ensure efficiency and clear separation of responsibilities:

1. **Skeleton File (`datacollectordaem.py`)**: This file contains the main daemon logic, handling the initialization, signal processing, and execution flow.
2. **Function File (`datacollectorfunc.py`)**: This file includes the core functions for data collection, processing, and database interactions, such as executing the `nvidia-smi` command and inserting data into the SQLite database.
3. **Configuration File (`config.py`)**: This file holds configuration settings and parameters, such as the frequency of data collection and the number of iterations.



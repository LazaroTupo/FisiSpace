## Requirements

Make sure you have the following installed before you start:

- Python 3.10 or higher
- Pip (for managing dependencies)

## Installation

1. Clone this repository to your local machine or download the files.

   ```bash
   git clone https://github.com/LazaroTupo/FisiSpace.git
   cd FisiSpace
   ```

## Create a Virtual Environment to Avoid Conflicts with Your Other Projects

1. Run the following command to create it:

   ```
   python -m venv .venv
   ```

2. To activate it:

   - On Linux (bash):

   ```
   source .venv/bin/activate
   ```

   - On Linux (nushell):

   ```
   cp activate.nu .venv/bin/activate.nu
   source .venv/bin/activate.nu
   ```

   - On Windows:

   ```
   .venv\Scripts\activate
   ```

3. Install the project dependencies:

   ```
   pip install -r requirements.txt
   ```

## Execution

To start the FastAPI server, run the following command:

    uvicorn main:app --reload

Route: http://127.0.0.1:8000/docs

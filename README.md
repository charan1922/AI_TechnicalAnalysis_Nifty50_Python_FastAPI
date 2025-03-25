# StockAnalysis_Nifty_50_Python_FastAPI_OpenAI

## Setting Up the Virtual Environment

Follow these steps to set up a virtual environment for this project:

1. **Install Python**  
   Ensure you have Python 3.7 or higher installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Create a Virtual Environment**  
   Open a terminal and navigate to the project directory. Run the following command to create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**

   - On **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**  
   After activating the virtual environment, install all dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. **Deactivate the Virtual Environment**  
   When you're done working, deactivate the virtual environment by running:
   ```bash
   deactivate
   ```

## Running the Application

After setting up the virtual environment and installing dependencies, you can run the FastAPI application using the following command:

```bash
fastapi dev main.py
```

Once the server starts, you can access the application at:

- **Base URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc API Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Additional Notes

- **Pydantic**: Used for data validation and settings management in FastAPI.
- **PyMongo**: Used for interacting with MongoDB.
- **OpenAI**: Used for integrating OpenAI APIs.

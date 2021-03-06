# Steps for Cluster Inference Testing

Notes:
* **__NOT__** COMPATIBLE WITH `python` 3.8 AND ABOVE
* Each generation request takes around 20 seconds


1. Copy the trained model to working directory. Replace `[PATH_TO_MODEL_DIR]` with path ending in the model directory
   
   ```sh
   mkdir -p ./checkpoint/run1/ && cp -r [PATH_TO_MODEL_DIR] ./checkpoint/run1/
   ```

2. Install `poetry`
   <br/><br/>
   Linux/MacOS:
   ```sh
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
   ```  
   Windows (PS):
   ```PS
   (Invoke-WebRequest -Uri `
   https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py `
   -UseBasicParsing).Content | python -
   ```
   
3. Restart terminal or open a new shell and verify `poetry` installation
   ```sh
   poetry -V
   ``` 

4. Install dependencies
   ```sh
   poetry install
   ```

5. Set up request authentication by setting `AUTH_KEY` in `config.py` to an authentication key. Also add this auth key to the bot's `config.py`
   ```sh
   (config.py) AUTH_KEY = [AUTH_KEY]
   ```

6. Start the `fastapi` server on port 8000
   ```sh
   poetry run python3 main.py 
   ```
   
7.  Send GET request
    ```sh
    curl "[IP]:8000/generate?input=[INPUT]&auth=[AUTH_KEY]"
    ```

# Current Configuration

Since the server that we have has sub-optimal performance, it is currently configured as backup to Cloud Run (ironic) with 774M.
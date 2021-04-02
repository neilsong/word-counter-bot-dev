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

5. Start the `fastapi` server on port 8000
   ```sh
   poetry run python3 main.py 
   ```
   
6.  Send GET request
    ```sh
    curl "[IP]:8000/generate?input=[INPUT]"
    ```
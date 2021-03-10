# Steps for Cluster Inference Testing

Notes:
* **__NOT__** COMPATIBLE WITH `python` 3.8 AND ABOVE
* Each generation request takes around 20 seconds

1. Create an ngrok account at https://dashboard.ngrok.com/signup

2. Get the auth token at https://dashboard.ngrok.com/auth/your-authtoken
   
3. Set `NGROK_AUTH_TOKEN` in config.py to the auth token
   ```sh
   config.py: NGROK_AUTH_TOKEN = "AUTH_TOKEN"
   ```

4. Copy the trained model to working directory. Replace `[PATH_TO_MODEL_DIR]` with path ending in the model directory
   
   ```sh
   mkdir -p ./checkpoint/run1/ && cp -r [PATH_TO_MODEL_DIR] ./checkpoint/run1/
   ```

5. Install `poetry`
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
   
6. Restart terminal or open a new shell and verify `poetry` installation
   ```sh
   poetry -V
   ``` 

7. Install dependencies
   ```sh
   poetry install
   ```

8. Start the `fastapi` server
   ```sh
   poetry run python3 main.py 
   ```

9. Find `ngrok` backend url from `std` at the line
   ```sh
   Public URL: [NGROK_URL]
   ```
   
10. Send GET request
    ```sh
    curl "[NGROK_URL]/generate?input=[INPUT]"
    ```
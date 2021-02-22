# Inference Pipeline

Two types of inference pipelines for different sized pre-trained GPT-2 models exposed via a text-generation API endpoint.

## Cloud Run Inference

Container-based inference, model bundled into docker image. Use for models smaller than 1558M. Follow https://github.com/minimaxir/gpt-2-cloud-run (Cloud Run RAM limit is now 8GB). 

## Cluster Inference

Use on a cluster/instance with more than 10GB of RAM. Can run any GPT-2 model.

## Steps for Cluster Inference Testing

**__NOT__** COMPATIBLE WITH PYTHON 3.8 AND ABOVE.

1. Create an ngrok account at https://dashboard.ngrok.com/signup

2. Get the auth token at https://dashboard.ngrok.com/auth/your-authtoken

3. Copy the trained model to working directory. Replace `[PATH_TO_MODEL_DIR]` with path to the model directory
   
   ```sh
   mkdir -p ./checkpoint/run1/ && cp -r [PATH_TO_MODEL_DIR] ./checkpoint/run1/
   ```

4. Run first-time setup. Replace `[NGROL_AUTH_TOKEN]` with the auth token.
   ```sh
   ./setup.sh [NGROL_AUTH_TOKEN]
   ```

5. Run startup script
   ```sh
    screen -d -m start.sh
   ```

6. You may have to enter `root` password. Find ngrok backend url by attaching API `screen`
    ```sh
    screen -r
    ```

7. Detach from `screen`  
   <kbd>CTRL</kbd>+<kbd>A</kbd>, <kbd>CTRL</kbd>+<kbd>D</kbd>
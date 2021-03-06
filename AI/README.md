# AI Component

These are both the training and inference piplines for the AI componenent of the Word Counter Bot. The model is currently a custom, fine-tuned version of [OpenAI's](https://openai.com) [GPT-2](https://openai.com/blog/better-language-models/) via [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple). It is trained on Discord message data.

## Training Pipeline

A Colab Jupyter Notebook highly based off of the ["Train a GPT-2 Text-Generating Model w/ GPU For Free"](https://colab.research.google.com/drive/1VLG8e7YSEwypxU-noRNhsv5dW4NfTGce) notebook by [Max Woolf.](https://minimaxir.com/) 
 - All execution is done in Google Colab. 
 - Available at (TBA)

## Inference Pipeline

3 types of inference pipelines for different sized pre-trained GPT-2 models exposed via a text-generation API endpoint. The live bot is currently using the `MEDIUM` GPT-2 model (355M params) and a Cloud Run inference with a Cloud Build CI/CD pipeline.
## Cloud Run Inference

Container-based inference, model bundled into docker image. Use for models smaller than 355M and smaller. Compared to https://github.com/minimaxir/gpt-2-cloud-run, this image uses `fastapi` instead of `starlette`. Go to that repo for additional information/documentation.
 - Cloud Run RAM limit is now 8GB
 - This image is optimized to use 355M on 8GB
   - `generate_count` may have to be used if testing with a different configuration
   - 774M runs OOM on 8GB
## Colab Inference

This exposes a HTTP API running on Colab through `ngrok`. Understand that this is most convenient for dev and testing purposes only since it is not a permanent solution. 
 - All execution is done in Google Colab. 
 - Available at https://colab.research.google.com/drive/1kHkTNKqObPwNCIx4Gtb_Jk7-EO4tthD-?usp=sharing
 - No OOM considerations in place
## Cluster Inference

Use on a cluster/instance with more than 16GB of RAM (32GB to be safe). Can run any version of GPT-2.
 - Main benefit of GPU utilization

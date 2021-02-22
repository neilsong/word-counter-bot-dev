# AI Component

These are both the training and inference piplines for the AI componenent of the Word Counter Bot. The model is currently a custom, fine-tuned version of [OpenAI's](https://openai.com) [GPT-2](https://openai.com/blog/better-language-models/) via [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple). It is trained on Discord message data.

## Training Pipeline

A Colab Jupyter Notebook highly based off of the ["Train a GPT-2 Text-Generating Model w/ GPU For Free"](https://colab.research.google.com/drive/1VLG8e7YSEwypxU-noRNhsv5dW4NfTGce) notebook by [Max Woolf.](https://minimaxir.com/) 
 - All execution is done in Google Colab. 
 - Available at (TBA)

## Inference Pipeline

Two types of inference pipelines for different GPT-2 model sizes. This bot is currently using the max GPT-2 size (1558M), so it is using cluster inference. More details in `./Inference Pipline/`
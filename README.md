# word-counter-bot (Dev)
![GitHub top language](https://img.shields.io/github/languages/top/neilsong/word-counter-bot-dev)
[![DeployCommit](https://github.com/neilsong/word-counter-bot-dev/actions/workflows/DeployCommit.yml/badge.svg)](https://github.com/neilsong/word-counter-bot-dev/actions/workflows/DeployCommit.yml)
[![Lint](https://github.com/neilsong/word-counter-bot-dev/actions/workflows/black.yml/badge.svg)](https://github.com/neilsong/word-counter-bot-dev/actions/workflows/black.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Kanban: https://app.gitkraken.com/glo/board/X_1FdLw5GgAS4oFE  
Release: https://github.com/neilsong/word-counter-bot
## Description

**A Python Discord Bot for Word Counting, Linguistics Analytics, and Vocabulary Insights**

Currently, we are trying our best to deliver a stable beta release with all the features we wish to include. This repo is used for all development and testing of the bot.

## Features

  1. Provide unique insight and analytics into the vocabulary of a server.
        - Leaderboards of users of a word
        - Leaderboards of most common words

  2. An AI text-generation model that will send a conversation about a topic based off of collected Discord message data.

  3. (Next major feature) Create a web app that serves a dashboard with insights, charts, and analytics 

## Steps for testing

  1. Create your own MongoDB cluster - you can create a free sandbox one at https://mongodb.com/atlas or locally host

  2. Add your discord bot token, MongoDB connection string, and Discord user id to `config.py`

  3. Install `poetry`
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
   
  4. Restart terminal or open a new shell and verify `poetry` installation
     ```sh
     poetry -V
     ``` 

  5. Install dependencies (Use `--no-dev` argument if only testing)
  
     ```sh
     poetry install
     ```
                
  6. (Dev only) Install `pre-commit` hooks
  
     ```sh
     poetry run pre-commit install
     ```

  7. Run bot  
  
     ```sh
     poetry run python main.py
     ```

## Notes

 - GETTING THE BOT ON MORE SERVERS IS THE TOP PRIORITY.
   - We're trying to get more training data and usage.
   - We will start worrying about performance and sharding if the bot is on enough servers.
 - Pull requests are always welcome. As always, feel free to open issues.
 - If you want to contribute, take a look at `SCHEMAS`. It will help you get started a lot more quickly.
 - `disputils` is bundled locally because I was too lazy to open an issue/PR about custom embed footers. If you want to, go ahead.
   - Of course, all credit to https://github.com/LiBa001/disputils
 - Training is manual because we use Google Colab and are poor.
 - Automated inference is slow because we use Google Cloud Run and are poor.
 - Anthony and I are high school students, so we are
   - Poor
   - Time-constrained
   - Stressed
   - Always online on Discord
   
## Contributors
Neil Song - https://github.com/neilsong  
Anthony Wang - https://github.com/Honyant  
Byron Li - https://github.com/ByronLi8565

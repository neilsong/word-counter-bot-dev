# word-counter-bot (Dev)

[![DeployCommit](https://github.com/neilsong/word-counter-bot-dev/actions/workflows/DeployCommit.yml/badge.svg)](https://github.com/neilsong/word-counter-bot-dev/actions/workflows/DeployCommit.yml)

Kanban: https://app.gitkraken.com/glo/board/X_1FdLw5GgAS4oFE  
Release: https://github.com/neilsong/word-counter-bot
## Description

**A Python Discord Bot for Word Counting, Linguistics Analytics, and Vocabulary Insights**

Currently, we are trying our best to deliver a stable beta release with all the features we wish to include. This repo is used for all development and testing of the bot.

## Features

  1. Provide insight and analytics into the unique language of this server
        - Leaderboard of most common words in the server
        - Your own personal leaderboard of most common words

  2. (Next major feature) Create an AI model that will mimic your style to send a message you would probably send on command

  3. (Very far off) Create a web app that serves a dashboard with insights, charts, and analytics 

## Steps for testing

  1. Create your own MongoDB cluster - you can create a free sandbox one at https://mongodb.com/atlas or locally host

  2. Add your discord bot token, MongoDB connection string, and Discord user id to `config.py`

  3. (Optional) Setup Virtual Environment  
     
     ```sh
     python3 -m venv venv
     ```
     
  4. (Optional) Activate Virtual Environment
  
     ```sh
     Linux/MacOS: source venv/bin/activate
     ```  
     ```sh
     Windows (CMD): venv\Scripts\activate.bat
     ```  
     ```sh
     Windows (PS): venv\Scripts\Activate.ps1
     ```
                
  5. Install dependencies  
  
     ```sh
     pip3 install -r requirements.txt
     ```

  6. Run bot  
  
     ```sh
     python3 main.py
     ```
   
## Contributors
Neil Song - https://github.com/neilsong  
Anthony Wang - https://github.com/Honyant  
Byron Li - https://github.com/ByronLi8565

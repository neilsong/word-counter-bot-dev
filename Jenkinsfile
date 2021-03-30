pipeline {
  agent any
  stages {
    stage('Deploy') {
      steps {
        sh '''#! /bin/bash
cd /word-counter-bot-dev
git pull
screen -d -m .github/workflows/execution.sh'''
      }
    }

  }
}
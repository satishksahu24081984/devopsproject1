pipeline {
  agent any
  triggers {
    githubPush()
  }
  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/Sanjeev14-yadav/cicd-scrap-project.git'
      }
    }
    stage('Print Message') {
      steps {
        echo 'Build Triggered from GitHub Push! now webhook successfully done pleae push this message'
      }
    }
  }
}

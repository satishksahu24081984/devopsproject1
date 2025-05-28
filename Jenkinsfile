pipeline {
  agent any
  triggers {
    pollSCM('* * * * *')  // Check for changes every minute
  }
  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/Sanjeev14-yadav/cicd-scrap-project.git'
      }
    }
    stage('Test Trigger') {
      steps {
        echo 'Triggered by polling GitHub repo!'
      }
    }
  }
}

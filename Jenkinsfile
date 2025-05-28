pipeline {
  agent any
  stages {
    stage('Clone') {
      steps {
        git 'https://github.com/your-org/your-repo.git'
      }
    }
    stage('Build Images') {
      steps {
        sh 'docker build -t your-dockerhub-user/frontend:latest -f Dockerfile.frontend .'
        sh 'docker build -t your-dockerhub-user/backend:latest -f Dockerfile.backend .'
      }
    }
    stage('Push Images') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PWD', usernameVariable: 'DOCKER_USER')]) {
          sh 'echo "$DOCKER_PWD" | docker login -u "$DOCKER_USER" --password-stdin'
          sh 'docker push your-dockerhub-user/frontend:latest'
          sh 'docker push your-dockerhub-user/backend:latest'
        }
      }
    }
    stage('Ansible Deploy') {
      steps {
        sh 'ansible-playbook -i ansible/inventory ansible/playbook.yml'
      }
    }
  }
}

node {
    stage('clean') {
        sh 'pwd'
        sh './staging/cleanup.sh'

    }

    stage('Unit Tests') {

    }
    
    stage('Build and send images to GCP CR') {
        sh './staging/build.sh'
    }

    stage('Deploy to GCP staging') {
        sh './staging/deploy.sh'
    }

    stage('Integration Test') {

    }
}

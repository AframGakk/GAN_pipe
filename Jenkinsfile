node {
    def git = checkout scm
    stage('clean') {
        echo "${git.GIT_COMMIT}"
        sh 'ls -ln'
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

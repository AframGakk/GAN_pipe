node {
    stage('clean') {
	    steps {
	        sh './staging/cleanup.sh'
	    }
    }

    stage('Unit Tests') {
    	steps {

      	}
    }
    
    stage('Build and send images to GCP CR') {
        steps {
            sh './staging/build.sh'
        }
    }

    stage('Deploy to GCP staging') {
        steps {
            sh './staging/deploy.sh'
        }
    }

    stage('Integration Test') {
        steps {

        }
    }
}

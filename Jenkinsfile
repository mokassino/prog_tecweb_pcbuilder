pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                withPythonEnv('python') {
                    sh "python --version"
                    sh "pip -V"
                }

                withPythonEnv('/opt/venv/pcbuilder') {
                    // Test for ManagedVirtualenv
                    sh "python --version"
                    sh "pip -V"
                }
            }
          
        }
        stage('Build') {
            withPythonEnv('/opt/venv/pcbuilder') {
                echo "Installing python dependencies..."
                sh "pip install -r requirements.txt"
            }
        }
        stage('Deploy'){
            withPythonEnv('/opt/venv/pcbuilder'){
                flask run
            }
        }
    }
}

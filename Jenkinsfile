pipeline {
    agent any 
    triggers {
        // 看要用定時 trigger 還是用 pr trigger
        // cron('0 11 11 * *', false, 'Asia/Taipei')
        cron('0 11 11 * *')
    }

    environment {
        // set up your jenkins credentials
        ENV_FILE = credentials('ENV_FILE') 
    }

    stages {
        // stage('Set up env') {
        //     steps {
        //         script {
        //             // sh 'python3 -m pip install --upgrade pip'
        //             sh 'pip install -r requirement.txt'
        //         }
        //     }
        // }
        stage('Test') {
            steps {
                // script {
                    sh 'pip3 install pytest'   
                    sh 'python3 -m pytest ./test_api/test_api_login.py'
                // }
            }
        }
    }
}

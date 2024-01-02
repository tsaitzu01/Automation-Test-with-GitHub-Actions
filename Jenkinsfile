pipeline {
    agent any 
    triggers {
        // 看要用定時 trigger 還是用 pr trigger
        // cron('0 11 11 * *', false, 'Asia/Taipei')
        cron('0 11 11 * *')
    }

    environment {
        // set up your jenkins credentials
        ENV = credentials('api-env') 
    }


    stages {
        // set up your stages
        stage('Set up env'){
          steps{
            sh 'python -m pip install --upgrade pip'
            sh 'pip install requirment.txt'
          }
        }

        stage('Run Test'){
          steps{
            sh 'python3 -m pytest ./test_api/test_api_login.py'
          }
        }
    }
}

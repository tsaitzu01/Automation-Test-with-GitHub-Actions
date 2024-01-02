pipeline {
    agent any 
    triggers {
        // 看要用定時 trigger 還是用 pr trigger
        // cron('0 11 11 * *', false, 'Asia/Taipei')
        cron(spec: '0 11 11 * *', timezone: 'Asia/Taipei')
    }

    environment {
        // set up your jenkins credentials
        ENV = credentials('ENV') 
    }


    stages {
        // set up your stages
        stage('Set up env'){
          steps{
            sh 'pip3 install --upgrade pip'
          }
        }

        stage('Run Test'){
          steps{
            sh 'python3 -m pytest ./test_api/test_api_login.py'
          }
        }
    }
}

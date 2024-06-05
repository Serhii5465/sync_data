@Library('PrepEnvForBuild') _

pipeline{
    agent {
        label 'master'
    }
    
    options { 
        skipDefaultCheckout()
    }

    parameters {
        choice choices: ['Win10_MSI', 'Win10-Dell'], description: 'Choose an agent for deployment', name: 'AGENT'
    }

    stages {
        stage('Check status agent'){
            steps{
                CheckAgent("${params.AGENT}")
            }
        }

        stage('Git checkout'){
            steps {
                git branch: 'main', 
                checkout scmGit(branches: [[name: 'main']],
                extensions: [], 
                userRemoteConfigs: [[url: 'sync_data_repo:Serhii5465/sync_data.git']])

                stash includes: '**/*.py', name: 'src'
            }
        }

        stage ('Deploy'){
            agent {
                label "${params.AGENT}"
            }
            steps {
                unstash 'src'
                bat returnStatus: true, script: 'Robocopy.exe /E /copyall . D:\\system\\applications\\cygwin64\\home\\raisnet\\scripts\\sync_data'
            }
        }
    }
}
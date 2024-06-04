@Library('PrepEnvForBuild') _

pipeline{
    agent {
        label 'master'
    }
    
    options { 
        skipDefaultCheckout()
        timestamps()
    }

    parameters {
        choice choices: ['Win10_MSI', 'Win10-Dell'], description: 'Choose an agent for deployment', name: 'AGENT'
        credentials credentialType: 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey', defaultValue: '', name: 'GIT_REPO_CRED', required: true
    }

    stages {
        stage('Check status agent/git cred'){
            steps{
                CheckAgent("${params.AGENT}")
                CheckGitCred("$params.GIT_REPO_CRED")
            }
        }

        stage('Git checkout'){
            steps {
                git branch: 'main', 
                credentialsId: "${params.GIT_REPO_CRED}", 
                poll: false, 
                url: 'git@github.com:Serhii5465/sync_data.git'

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
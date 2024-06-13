@Library(['PrepEnvForBuild', 'DeployWinAgents']) _

node('master') {
    def raw = libraryResource 'configs/sync_data_repo.json'
    def config = readJSON text: raw
    DeployArtifactsPipelineWinAgents(config)
}
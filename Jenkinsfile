@Library(['PrepEnvForBuild', 'DeployWinAgents']) _

node('master') {
    def config = [
        git_repo_url : "sync_data_repo:Serhii5465/sync_data.git",
        git_branch : "main",
        stash_includes : "**/*.py",
        stash_excludes : "",
        command_deploy : "robocopy /E . D:\\system\\scripts\\sync_data",
        func_deploy : ""
    ]

    DeployArtifactsPipelineWinAgents(config)
}
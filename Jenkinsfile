@Library(['PrepEnvForBuild', 'DeployWinAgents']) _

node('master') {
    def config = [
        git_repo_url : "sync_data_repo:Serhii5465/sync_data.git",
        git_branch : "main",
        stash_includes : "**/*.py",
        stash_excludes : "",
        command : "robocopy /E /copyall . D:\\system\\applications\\cygwin64\\home\\raisnet\\scripts\\sync_data"
    ]

    DeployArtifactsPipelineWinAgents(config)
}
@Library(['PrepEnvForBuild', 'DeployWinAgents']) _

node('master') {
    def config = [
        platform: "win32",
        git_repo_url : "git@github.com:Serhii5465/sync_data.git",
        git_branch : "main",
        git_cred_id : "sync_data_repo_cred",
        stash_includes : "**/*.py",
        stash_excludes : "",
        command_deploy : "robocopy /E . D:\\system\\scripts\\sync_data",
        func_deploy : ""
    ]

    DeployArtifactsPipelineOnAgents(config)
}
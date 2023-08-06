dockerfile_path=$1
docker_config_name=$2
docker_registry_url=$3

if [ $# -ge 5 ]
  then
    git_remote_url=$4
    git_commit_hash=$5
fi

cd $dockerfile_path
mkdir src
cd src

if [ -v git_remote_url ]
  then
    git init
    git remote add origin $git_remote_url
    GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no" git fetch --depth 1 origin $git_commit_hash
    git checkout FETCH_HEAD
fi

podman build -f Dockerfile $dockerfile_path --log-level=debug -t $docker_config_name
podman push localhost/$docker_config_name $docker_registry_url/$docker_config_name

set -xe

dockerfile_path=$1
docker_registry_url=$2
docker_image_hash=$3

if [[ $# -ge 5 ]]
  then
    git_remote_url=$4
    git_commit_hash=$5
fi

cd $dockerfile_path/src

if [[ -v git_remote_url ]]
  then
    git init
    git remote add origin $git_remote_url
    GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no" git fetch --depth 1 origin $git_commit_hash
    git checkout FETCH_HEAD
fi

if [[ $(podman images $docker_image_hash | wc -l) -lt 2 ]]
  then
    echo "building new image..."
    podman build -f Dockerfile $dockerfile_path --log-level=debug -t $docker_image_hash
    podman push localhost/$docker_image_hash $docker_registry_url/$docker_image_hash
  else
    echo "image present in cache, exiting..."
fi

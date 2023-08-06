# install global
    pip install gosu

# per project init
    pre-commit install

# enable local github build
## enable docker tcp socket
    # add to /etc/docker/daemon.json
    {"hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]}

    # replace in /lib/systemd/system/docker.service
    ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
    # with
    ExecStart=/usr/bin/dockerd --containerd=/run/containerd/containerd.sock

    systemctl daemon-reload
    sudo systemctl restart docker.service

## install gitlab-ci-local
    npm install -g gitlab-ci-local
https://github.com/firecow/gitlab-ci-local

## run local gitlab runner build
    gosu ci local

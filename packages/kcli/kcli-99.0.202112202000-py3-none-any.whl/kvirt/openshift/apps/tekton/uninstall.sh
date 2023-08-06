VERSION={{ previous/{{ tekton_version }} if tekton_version != 'latest' else 'latest' }}
NOTAG={{ '.notags.yaml' if engine|default('containerd') == 'crio' else '' }}
kubectl delete -f https://storage.googleapis.com/tekton-releases/pipeline/$VERSION/release.yaml$NOTAG

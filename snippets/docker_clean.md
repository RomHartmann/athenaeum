Clean shit up

```bash
alias dockerclean='docker images -f '\''dangling=true'\'' -q | xargs docker rmi && docker ps -f '\''status=exited'\'' -q | xargs docker rm'

docker system prune --volumes
```


Sort and count docker images by name

```bash
docker images | awk '{print $1}' | sort | uniq -c | sort -nr
```

Delete images by name

```bash
docker images | grep my-image-name | awk '{print $1 ":" $2}' | xargs docker rmi
```







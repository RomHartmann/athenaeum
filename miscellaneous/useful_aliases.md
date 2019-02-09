# Useful Aliases

## Python

```bash
alias unittest="python3.6 -m unittest discover -p '*_test.py'"
```

### Docker

```bash
alias dockerclean="docker images -f 'dangling=true' -q | xargs docker rmi && docker ps -f 'status=exited' -q | xargs docker rm"
```

### AWS

```bash
alias getssmpath="aws ssm --profile data --region us-east-1 --with-decryption get-parameters-by-path --recursive --path"
alias getssmname="aws ssm --profile data --region us-east-1 --with-decryption get-parameter --name"
```



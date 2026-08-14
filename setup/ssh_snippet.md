```bash
ssh -i laelgelc20260117.pem \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=4 \
  -o ConnectTimeout=60 \
  ubuntu@
```
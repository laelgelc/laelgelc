# SSH into a `us-east-1` instance

```bash
cd ../work
ssh -i laelgelc20260617.pem \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=4 \
  -o ConnectTimeout=60 \
  ubuntu@
```

# SSH into a `sa-east-1` instance

```bash
cd ../work
ssh -i laelgelc20260117.pem \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=4 \
  -o ConnectTimeout=60 \
  ubuntu@
```
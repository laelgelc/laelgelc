```bash
aws s3 cp . s3://laelgelc/cl_st1_carol/ \
  --recursive \
  --exclude "*" \
  --include "*.wav"
```
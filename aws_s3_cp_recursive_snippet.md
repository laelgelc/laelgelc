# Simple `aws s3 cp` command

```shell script
aws s3 cp s3://laelgelc/cl_st1_carol/ . \
  --recursive \
  --exclude "*" \
  --include "*.wav"
```

# Advanced `aws s3 sync` command

**User**

The processing is done! Now, I need to transfer the *.wav files (985 files) from the following directory to my local development machine via AWS S3. I intend to copy the files to the `gelc-proc-1` bucket (that is empty) and then copy them to the same directory in my development machine. Can you remind me of the AWS commands?

```text
ubuntu@ip-172-31-5-251:~/cl_st1_claudia/cl_st1_ph1_claudia/corpus/01_music_videos_audio/audio$ pwd
/home/ubuntu/cl_st1_claudia/cl_st1_ph1_claudia/corpus/01_music_videos_audio/audio
ubuntu@ip-172-31-5-251:~/cl_st1_claudia/cl_st1_ph1_claudia/corpus/01_music_videos_audio/audio$ aws s3 ls
2026-04-23 19:52:46 gelc-proc-1
2026-04-23 16:20:33 gelc-raw-1
2026-04-23 19:06:21 gelc-unarch-1
2026-04-23 17:16:19 gelcawsemr
2026-04-23 18:46:30 laelgelc
2026-04-23 18:47:30 laelgelclatexws
2026-04-23 17:24:10 laelgelcpublic
2026-07-23 18:36:52 lmda-app
2026-04-23 18:15:26 twdnld
2026-04-23 17:47:37 twunarch
ubuntu@ip-172-31-5-251:~/cl_st1_claudia/cl_st1_ph1_claudia/corpus/01_music_videos_audio/audio$ 
```

**AI Assistant**

That is great news! Moving the files via S3 using the `aws s3 sync` command is definitely the most efficient way to handle this.

Here are the commands you need for both environments.

## Step 1: Upload from the EC2 instance to S3

Run this on your **EC2 instance** to copy all the `.wav` files into a folder named `audio` inside your empty `gelc-proc-1` bucket:

```shell script
cd ~/cl_st1_claudia/cl_st1_ph1_claudia/corpus/01_music_videos_audio/audio
aws s3 sync . s3://gelc-proc-1/audio/ --exclude "*" --include "*.wav"
```

*(The `--exclude "*"` followed by `--include "*.wav"` ensures that absolutely only the WAV files are transferred, just to be on the safe side).*

## Step 2: Download from S3 to your local machine

Once the upload finishes, open a terminal on your **local development machine**, navigate to the corresponding directory, and sync the files down:

```shell script
cd ~/PycharmProjects/cl_st1_claudia/cl_st1_ph1_claudia/corpus/01_music_videos_audio/audio
aws s3 sync s3://gelc-proc-1/audio/ .
```

**User**

What exactly this `sync` command do? If I have a few existing files in my local machine, I guess they are not overwritten if they are identical, right?

**AI Assistant**

You are exactly right! 

The `aws s3 sync` command is smart. Instead of blindly copying everything, it compares the source (the S3 bucket) and the destination (your local machine). 

Here is exactly how it decides what to do:
1. **Size and Timestamp Check**: It compares the file sizes and the "last modified" timestamps of the files in S3 against the ones on your local machine.
2. **Skips Identical Files**: If a file already exists locally with the same size and it isn't older than the version in S3, `sync` will completely skip downloading it. 
3. **Downloads Only What's Needed**: It will only download a file if it is missing locally, or if the version on S3 has a different file size or a newer modified timestamp.

This makes `sync` incredibly efficient. If your download gets interrupted halfway through, you can just run the exact same `aws s3 sync` command again. It will instantly skip the 500 files you already downloaded and just resume downloading the rest.

## Step 3: Clean up the bucket

**User**

It's done! How can I clean up the bucket?

**AI Assistant**

To clean up and remove all the files you uploaded to your S3 bucket without deleting the bucket itself, you can use the `rm` command with the `--recursive` flag.

Run this command from either your local machine or the EC2 instance:

```shell script
aws s3 rm s3://gelc-proc-1/ --recursive
```

This will go through and delete every file and folder inside the `gelc-proc-1` bucket. 

*(Note: If you actually wanted to delete the entire bucket itself after emptying it, you would use `aws s3 rb s3://gelc-proc-1/ --force`, but usually it's best to just empty it so you can reuse the bucket for the next batch of work!)*
# AAI Face Search DB Builder
A simple Python script to help clients to add images in a local directory, Amazon S3, or Alibaba Cloud OSS to their Face Search database by calling the db-build API.

## Installation
```
pip install aai-face-search-db-builder
```
## How to use
After installation, run the following command to see the required arguments to pass.
```
$ dbbuilder -h
```

## Notes
* The script will create a sqlite3 database called `images.db` to keep track of completed tasks.
# Syncr-Worker
Worker for the Syncr app, still in development

You can see the main application [here](https://github.com/Zeptiny/Syncr).

# Routes needed:
The worker will act in a "passive" way, meaning the it will NOT send any information to the Controller. The Controller will request the information from the Worker.

It will be less efficient, however, in my mind will also be easier to create. They won't be transferring a lot of information anyway.

## Create Job:
Will receive all the information needed for the job, including:
  - Rclone remote information
  - Restic and related information
  - User

Will return an UUID to query the job

## Query Job
Will receive the job UUID, returning it's stats

## Obscure
Needed for rclone when obscuring the password
Can also be implemented in the controller, if I find a way to do it without a rclone instance.

# Authentication:
Of course, everything will be encrypted with SSL.

Authenticate the worker with the controller, to avoid someone sneaking information, if they, somehow, get the job UUID, while still making things simple:

Create a 256 bit key with openssl. Example: openssl rand -hex 32

- The controller will have one key stored for each worker.
- The worker will have that key as an environment variable.
- That key will need to be passed with each request.

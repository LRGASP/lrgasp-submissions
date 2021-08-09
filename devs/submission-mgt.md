# Submission management

## Evaluation queues (LRGASP challanges)
    * Challenge 1: iso_detect_ref (9614748)
    * Challenge 2: iso_quant (9614749)
    * Challenge 3: iso_detect_de_novo (9614750)

## Viewing submissions:

1. Go to Tables
1. Select the challenge queue to view submissions
1. As the table shows the results of a query, seeing added or removed submissions requires going back to
   Tables and reissuing the query.

## Downloading submissions for evaluation

To recursively download an submission using the submission id:

```
lrgasp-synapse-download 9713623 targetdir
```

The `lrgasp-synapse-download` program can also be used to download other
entities by synapse id:

```
lrgasp-synapse-download syn324578 targetdir
```

# Test Synapse projects setup

This also is a guide on how the actually LRGASP site is configured.

## Creating test challenge
This outlines the steps for creating the test projects.  This is also shows
how the LRGASP project would have been set up if done in one go.  Do not use
the word "LRGASP" in the project name, as these can be found by search and confused
people in the past.  We will call these "LRPLAY"

1. login into Synpase as yourself:
   % synapse login -u markd@ucsc.edu --rememberMe
1. create a new challenge project:
   % challengeutils create-challenge LRPLAY
   INFO:challengeutils.createchallenge:Created/Fetched Project LRPLAY (syn26023460)
1. go to the web app and create all evaluation queues pressing user icon,
   selecting `Challenges` and then selecting the LRPLAY project, then select `Challenge`.
1. Delete the default evaluation queue.. Create evaluation queues:
   "LRPLAY Challange 1", "LRPLAY Challange 2" and "LRPLAY Challange 3"
   Note the numeric queue ids (9614870, 9614868, 9614869).
1. setup a single round for each queue, which restricts a user to one submission
   % challengeutils set-evaluation-quota --num_rounds=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614870
   % challengeutils set-evaluation-quota --num_rounds=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614868
   % challengeutils set-evaluation-quota --num_rounds=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614869
1. Modified each evaluation queue to have the permissions:
   * LRPLAY Participants - Can submit
   * LRPLAY Evaluators - Administrator
1. go to `tables` and `Add Submission View` for each queue.
1. go to `Project Sharing Settings` and `Make Public`

## Creating test participant

A new account must be created for the test user using a different email
address and you must certify this user.  For this discussion, there
is a test user kermodei using a gmail address.

1. Login on to Synpase as test user.  Using a private browser window will allow being logged in as second user.
1. Create a team that will do the submissions "LRPLAYER Team"
1. All members of "LRPLAYER Team" must join "LRPLAY Participants"
1. Create a project that is use to upload the submission, "LRPLAYER Submit"
1. Add "LRPLAYER Team" to Project Sharing for "LRPLAYER Submit" with `Can edit & delete` permissions.
   This will allow any member of the "LRPLAYER Team" to submit.
1. Create tests/submit/test-conf.json from tests/submit/test-conf.jsontest-conf-template.json


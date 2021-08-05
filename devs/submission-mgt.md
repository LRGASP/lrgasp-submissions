# Submission management

## Evaluation queues (LRGASP challanges)
    * Challenge 1: iso_detect_ref (9614748)
    * Challenge 2: iso_quant (9614749)
    * Challenge 3: iso_detect_de_novo (9614750)

## Create evaluation queues
This is a Synapse sub-challange and LRGASP challange

For each queue
    * create each challenge in web-GUI
    * modify to allow "LRGASP Participants' to upload
    * modify to allow "LRGASP Organizers to score
    * set quota to allow only one submission per team for each queue with:
      challengeutils set-evaluation-quota --num_rounds=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614862

## Viewing submissions:
A submission view table is created for each submission


# Test Synapse projects

## Creating test challenge
This outlines the steps for creating the test projects.  This is also shows
how the LRGASP project would have been set up if done in one go.  Do not use
the word "LRGASP" in the project name, as these can be found by search and confused
people in the past.  We will call these "LRPLAY"

1. login into Synpase as yourself:
   % synapse login -u markd@ucsc.edu --rememberMe
2. create a new challenge project:
   % challengeutils create-challenge LRPLAY
   INFO:challengeutils.createchallenge:Created/Fetched Project LRPLAY (syn26023460)
3. go to teams and create a team "LRPLAY Evaluators"
4. go to the web app and create all evaluation queues pressing user icon,
   selecting `Challenges` and then selecting the LRPLAY project, then select `Challenge`.
5. Delete the default evaluation queue.. Create evaluation queues:
   "LRPLAY Challange 1", "LRPLAY Challange 2" and "LRPLAY Challange 3"
   Note the numeric queue ids (9614870, 9614868, 9614869).
6. setup a single round for each queue, which restricts a user to one submission
   % challengeutils set-evaluation-quota --num_rounds=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614870
   % challengeutils set-evaluation-quota --num_rounds=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614868
   % challengeutils set-evaluation-quota --num_rounds=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614869
7. Modified each evaluation queue to have the permissions:
   * LRPLAY Participants - Can submit
   * LRPLAY Evaluators - Administrator
6. go to `tables` and `Add Submission View` for each queue.
8. go to `Project Sharing Settings` and `Make Public`

## Creating test participant

A new account must be created for the test user using a different email
address and you must certify this user.  For this discussion, there
is a test user kermodei using a gmail address.

1. Login on to Synpase as test user.  Using a private browser window will allow being logged in as second user.
2. Create a team that will do the submissions "LRPLAYER Team"
3. All members of "LRPLAYER Team" must join "LRPLAY Participants"
3. Create a project that is use to upload the submission, "LRPLAYER Submit"
4. Add "LRPLAYER Team" to Project Sharing for "LRPLAYER Submit" with `Can edit & delete` permissions.
   This will allow any member of the "LRPLAYER Team" to submit.
4. Add "LRPLAY Evaluators" to Project Sharing for "LRPLAYER Submit" with `Can download` permissions.
   This will allow the evaluators to download submissions
5. Create tests/submit/test-conf.json from tests/submit/test-conf.jsontest-conf-template.json


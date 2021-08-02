# Submission management

## Evaluation queues (LRGASP challanges)
    * Challenge 1: iso_detect_ref (9614748)
    * Challenge 2: iso_quant (9614749)
    * Challenge 3: iso_detect_de_novo (9614750)

## Create evaluation queues
This is a Synapse sub-challange and LRGASP challange

For each queue
    * create each challange in web-GUI
    * modify to allow "LRGASP Participants' to upload
    * modify to allow "LRGASP Organizers to score
    * set quota to allow only one submission per team/user with:
      challengeutils set-evaluation-quota --sub_limit=1 --round_start=2021-06-01T00:00:00 --round_end=2021-10-01T23:59:59 9614862

## Viewing submissions:
A submission view table is created for each submission


# Testing lrgasp-submit-entry

Test challenge is markd-test

Test participant is kermodei (MarkD temp account) and test team is kermodei-lrgasp

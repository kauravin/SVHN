################################################################################

//for starting your instance
1. gcloud compute ssh instance-2 --zone us-west1-b 

//for mapping  the jupyter notebook running on the VM to the local port

2. gcloud compute ssh instance-2 --ssh-flag="-L" --ssh-flag="2222:localhost:8888" //make sure to check the port number of jupyter notebook

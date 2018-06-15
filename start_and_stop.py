#/usr/bin/python3
# written by Bhanu


import boto3
import sys


OPTION = (input("\nWant to start or stop a instance{start|stop}: ")).strip()
I_NAME = (input("\nName of instance: ")).strip()

def main():

    if OPTION == "start":
        startInstance()
    elif OPTION == "stop":
    	stopInstance()
    else:
    	print("Chose right option\n")

ec2 = boto3.client('ec2')
resource = boto3.resource('ec2')

def startInstance():
    print("Starting the instance...")

    for i in resource.instances.all():
        for tag in i.tags:
            if tag['Value'] == I_NAME:
                RI_ID = i.instance_id
                print(RI_ID)

    # change instance ID appropriately  
                try:
                    ec2.start_instances(
                        InstanceIds=[
                            RI_ID,
                        ],
                        DryRun=False
                    )
                except:
                    print("\nFailed because of wrong input. Please recheck and try")
                    sys.exit(1)

def stopInstance():
    print("Stopping the instance...")

    for i in resource.instances.all():
        for tag in i.tags:
            if tag['Value'] == I_NAME:
                RI_ID = i.instance_id
                print(RI_ID)

    # change instance ID appropriately  
                try:
                    ec2.stop_instances(
                        InstanceIds=[
                            RI_ID,
                        ],
                        DryRun=False
                    )
                except:
                    print("\nFailed because of wrong input. Please recheck and try")
                    sys.exit(1)


if __name__ == '__main__':
    main()
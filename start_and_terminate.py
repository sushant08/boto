import boto3
import boto3.ec2
import time
import sys

INPUT = (input('\nWant to create/rm instance : ')).strip()

if (INPUT == "create"):
    IMAGE = (input('\nEnter the image ID: ')).strip()
    I_TYPE = (input('\nEnter the instance type: ')).strip()
    KEY_NAME = (input('\nEnter keypair name: ')).strip()
    NEW_DISK = (input('\nDo you want to create new disk(Y/N): ')).strip()
    if (NEW_DISK == "Y"):
           EBS = int(input('\nEnter the volume size: '))
    elif(NEW_DISK == "N"):
           SNAP = (input('\nEnter existing volume snapshot name: ')).strip()
           EBS = int(input('\nEnter the volume size: '))
    else:
            print("Please enter valid value:(Y/N)")
            sys.exit(1)
    

elif(INPUT == "rm"):
    RI_NAME = (input('\nEnter name of instance you want to remove: ')).strip()
    R_VOL = (input('\nWant to retain volume Y/N:')).strip()
else:
    print("\nEnter correct option: create/rm")
    sys.exit(1)


ec2 = boto3.resource('ec2')

user_data_script = """#!/bin/bash
sudo mkfs.ext4 /dev/xvdh
sudo mkdir /vol
echo "/dev/xvdh /vol auto noatime 0 0" | sudo tee -a /etc/fstab
mount --all"""

def create():
    if(NEW_DISK ==  "Y"):
        createinstance = ec2.create_instances(
           BlockDeviceMappings=[
              {
                  'DeviceName': '/dev/xvdh',
                  'VirtualName': 'ephemeral',
                  'Ebs': {
                      'Encrypted': True,
                      'DeleteOnTermination': False,
 #                    'KmsKeyId': 'string',
 #                    'SnapshotId': 'string',
                      'VolumeSize': EBS,
                      'VolumeType': 'gp2'
                  },
             },
           ],
           ImageId=IMAGE,
           InstanceType=I_TYPE,
           KeyName= KEY_NAME,
           MaxCount=1,
           MinCount=1,
           SecurityGroupIds=[
              'sg-fe119188',
           ],
           SubnetId='subnet-846743bb',
           UserData=user_data_script,
           TagSpecifications=[
              {
               'ResourceType': 'instance',
               'Tags': [
                    {
                       'Key': 'Name',
                       'Value': 'Test'
                    },
                   ]
             },
           ],
     
        )
    else:
        createinstance = ec2.create_instances(
           BlockDeviceMappings=[
              {
                  'DeviceName': '/dev/xvdh',
                  'VirtualName': 'ephemeral',
                  'Ebs': {
                      'Encrypted': True,
                      'DeleteOnTermination': False,
 #                    'KmsKeyId': 'string',
                      'SnapshotId': SNAP,
                      'VolumeSize': EBS,
                      'VolumeType': 'gp2'
                  },
             },
           ],
           ImageId=IMAGE,
           InstanceType=I_TYPE,
           KeyName= KEY_NAME,
           MaxCount=1,
           MinCount=1,
           SecurityGroupIds=[
              'sg-fe119188',
           ],
           SubnetId='subnet-846743bb',
           UserData=user_data_script,
           TagSpecifications=[
              {
               'ResourceType': 'instance',
               'Tags': [
                    {
                       'Key': 'Name',
                       'Value': 'Test'
                    },
                   ]
             },
           ],
     
        )



    for instance in createinstance:
        time.sleep(5)
        print('\nLogin using private ip :',instance.private_ip_address)

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])      

client = boto3.client('ec2')

instance_vol = []
def rm():
    for i in ec2.instances.all():
        for tag in i.tags:
            if tag['Key'] == 'Name' and tag['Value'] == RI_NAME:
                RI_ID = i.instance_id
                if (RI_ID == None):
                    print("Instance with this tag don't exist")
                    sys.exit(1)
                print(RI_ID)
                volumes = i.volumes.all()
                for v in volumes:
                    if v.attachments(Device='/dev/xvdh':)
                       instance_vol.append(v.id)
                        
                response = client.terminate_instances(
                     InstanceIds=[
                          RI_ID,
                        ],
                        DryRun=False
                 )

            else:
                print("Instance with this tag don't exist")
        if(R_VOL == "Y"):
            time.sleep(20)
            for vm in instance_vol:
                try:
                    snapshot = ec2.create_snapshot(VolumeId=vm, Description="Snapshot frm instance")
                    print("Please save this snapshot id and use it in next instance creation: ", snapshot.id)
                except:
                    raise
        elif(R_VOL == "N"):
            for vm in instance_vol:
                volume = ec2.Volume(vm)
                response = volume.delete(
                    DryRun=True
                )
        else:
            print("You haven't choosed what to do with volume correctly")


{
'create':  create,
'rm':  rm,
}.get(INPUT)()










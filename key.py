import boto3

KEY_PAIR_NAME = (input('\nEnter keypair name you want to create: ')).strip()

ec2 = boto3.client('ec2')

try:
    response = ec2.create_key_pair(KeyName=KEY_PAIR_NAME)
    key = response['KeyMaterial']
    f = open(KEY_PAIR_NAME + ".pem","w+")
    f.write(key)
    f.close()
    print("\nYour key is create as '%s.pem' in current directory" % (KEY_PAIR_NAME))
except:
    print( '\033[91m' + "\nThis key name already exist. Please choose some other name for key" + '\033[0m')
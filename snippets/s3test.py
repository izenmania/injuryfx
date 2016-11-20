import boto3

client = boto3.client(
    's3',
    aws_access_key_id = "AKIAJWAN6PXW4LAPGY6Q",
    aws_secret_access_key = "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"
)

objs = client.list_objects(Bucket="injuryfx", Prefix="transactions/")

keys = []

for obj in objs['Contents']:
    if obj['Size'] > 0:
        keys.append(obj['Key'])


f = client.get_object(Bucket="injuryfx", Key=keys[0])
o = f['Body']

print(o.read())
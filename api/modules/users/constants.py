import uuid

UNIQUE_CODE = uuid.uuid4().hex
SUBJECT = 'Thank You for registering with us'
MESSAGE = 'Thank You for registering with us.This is the token number for future references ' + UNIQUE_CODE

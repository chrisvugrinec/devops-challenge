from flask_restplus import fields
from devops_restwrapper.api.restplus import api

bucketlister = api.model('AWS S3 Bucketlister', {
    'name': fields.String(required=True, description='AWS S3 Bucket name'),
})

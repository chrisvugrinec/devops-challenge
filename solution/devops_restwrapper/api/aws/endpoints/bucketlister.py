import logging

from flask import request
from flask_restplus import Resource
from devops_restwrapper.api.aws.serializers import bucketlister
from devops_backend.challenge import getBucketInfo
from devops_restwrapper.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('aws/bucketlister', description='list aws s3 buckets')


@ns.route('/list')
class AwsBucketLister(Resource):

    def get(self):
        """
        Lists your AWS Buckets and shows some basic info
        """
        return getBucketInfo()

@ns.route('/hello')
class AwsBucketLister(Resource):

    @api.marshal_list_with(bucketlister)
    def get(self):
        """
        Returns the famous hello message
        """
        return {'name':'hello world'}

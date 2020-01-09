import os
import time

import pulumi
from pulumi_gcp import cloudfunctions, storage,projects

project_name = os.getenv("project_name")
PATH_TO_SOURCE_CODE = "./functions"

def get_array_from_string(comma_separated_string):
    return comma_separated_string.split(",")

#you can set the confid by pulumi confif set mykey myvalue
config = pulumi.Config(name=None)
config_values = {
    "epic_secret_key":config.get("epic_secret_key")
}

bucket = None

assets = {}

function_dictionary = {
    "hello_function":"handle_hello_function",
}

#traverse_dir_recur(PATH_TO_SOURCE_CODE,assets)
archive = pulumi.FileArchive(PATH_TO_SOURCE_CODE)

def enable_apis(services):
    projects.Services(project=project_name,services=services,disable_on_destroy=False,resource_name="enable_dataorc_api_resources")

def create_function_and_output_end_url(function_name,entry_point):
    source_archive_object = storage.BucketObject(
        function_name,
        name="main.py-%f" % time.time(),
        bucket=bucket.name,
        source=archive)


    # Create the Cloud Function, deploying the source we just uploaded to Google
    # Cloud Storage.
    fxn = cloudfunctions.Function(
        function_name,
        entry_point=entry_point,
        environment_variables=config_values,
        region=os.getenv("region","us-east1"),
        runtime="python37",
        source_archive_bucket=bucket.name,
        source_archive_object=source_archive_object.name,
        trigger_http=True,available_memory_mb=256,project=project_name
        )

# Export the DNS name of the bucket and the cloud function URL.
    pulumi.export("bucket_name", bucket.url)
    pulumi.export("fxn_url", fxn.https_trigger_url)
    return fxn.https_trigger_url

def create_functions_from_function_dictionary(function_dictionary):
    return [create_function_and_output_end_url(function_path,function_name) for function_path,function_name in function_dictionary.items()]



def spawn_functions():
    global bucket
    bucket = storage.Bucket('dataorc-api-cloud-functions-new', force_destroy=False)
    function_external_urls = create_functions_from_function_dictionary(function_dictionary)
    print(function_external_urls)


spawn_functions()




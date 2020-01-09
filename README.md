
following library uses environment variables for secret as well configurable assets,

for pulumi use `pulumi set config configuration name configuration value`

Following are the steps to add new functions

1) Create a directory in functions which will contain for function
2) define a file entry_point.py, name is not mandatory just a convention
3) add a function in main.py in function directory which will call the entry function defined in entry_point.py
4) update the function mapping in __main__.py, this is for pulumi/terraform, mapping contains function name as key and function name in main.py defined in step above
5) ADD FUNCTION DOCUMENTATION IN OPENAPI format in dataorc_openapi.yaml, only then function will be exposed via dataorc endpoint
6) any common util function can go to util_function.py

Few pointers for creating function

* entry point functions receives flask request object
* checking of post, get request is upto the user
* authentication is happening at the endpoint level
* logging via print is available on gcp logs
* logging is also available via screwdriver client, currently using 
* if you have any extra dependency requirement, add your dependency in requirements.txt in functions folder


# Most Important 
DONT INCLUDE ANY SENSITIVE URL, PASSKEY, PARAMETERS in CODE , ALWAYS TRY TO READ FROM ENVIRONMENT VARIABLE(os.get_env)

adding of os environment variables can be done by 

`pulumi config set <os variable name> <os variable name>`



```commandline
pulumi config set gcp:project project_name
gcloud auth login
$ gcloud config set project <YOUR_GCP_PROJECT_HERE>
$ gcloud auth application-default login
export GOOGLE_APPLICATION_CREDENTIALS=cred_file_location

```
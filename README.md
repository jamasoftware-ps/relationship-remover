# Jama Software

## Relationship Remover

This script will allow the user to automatically delete relationships in Jama using the API.

#### Supported features:
* Delete all relationships in a specified project
* Delete all relationships in a specified project and of a specified relationship type ID

# Requirements
* [python 3.7+](https://www.python.org/downloads/)
* [Pipenv](https://docs.pipenv.org/en/latest/) 

## Installing dependencies 
 * Download and unzip the package contents into a clean directory.
 * execute `pipenv install` from the commandline.
 
## Usage
#### Config:
 * Open the config.ini file in a text editor and set the relevant settings for your environment.
 
 * Connections Settings:  These are the settings required to connect to Jama Connect via the REST API
   * `instnace url`: this is the URL of your Jama Instance ex: https://example.jamacloud.com
   * `using oauth`: Set to True or False.  If set to True, the client_id and client_secret variables will be used to log into 
   * `username`: The username or client id of the user
   * `password`: The password or client secret of the user
   Jama connect via OAuth


 * Import Settings:  These Settings inform the script how the data should be imported to Jama.
   * `project id`: This is a required field, specify the API ID of the project for this script to run against.
   * `relationship type`: This is an optional field, include this API ID of a relationship type if you only want 
   remove relationships of a specific type. Otherwise if this setting is not specified relationships of all types 
   will be removed.

#### Execution:
 * Open the terminal to the directory the script is in and execute the following:   
 ``` 
 pipenv run python relationship_remover.py
 ```
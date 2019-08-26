import configparser
import getpass
import sys
import time

from progress.bar import ChargingBar

from py_jama_rest_client.client import JamaClient, APIException


def init_jama_client():
    # do we have credentials in the config?
    credentials_dict = {}
    if 'CREDENTIALS' in config:
        credentials_dict = config['CREDENTIALS']
    try:
        instance_url = get_instance_url(credentials_dict)
        oauth = get_oauth(credentials_dict)
        username = get_username(credentials_dict)
        password = get_password(credentials_dict)
        jama_client = JamaClient(instance_url, credentials=(username, password), oauth=oauth)
        jama_client.get_available_endpoints()
        return jama_client
    except APIException:
        # we cant do things without the API so lets kick out of the execution.
        print('Error: invalid Jama credentials, check they are valid in the config.ini file.')
    except:
        print('Failed to authenticate to <' + get_instance_url(credentials_dict) + '>')

    response = input('\nWould you like to manually enter server credentials?\n')
    response = response.lower()
    if response == 'y' or response == 'yes' or response == 'true':
        config['CREDENTIALS'] = {}
        return init_jama_client()
    else:
        sys.exit()


def get_instance_url(credentials_object):
    if 'instance url' in credentials_object:
        instance_url = str(credentials_object['instance url'])
        instance_url = instance_url.lower()
        # ends with a slash? lets remove this
        if instance_url.endswith('/'):
            instance_url = instance_url[:-1]
        # user forget to put the "https://" bit?
        if not instance_url.startswith('https://') or instance_url.startswith('http://'):
            # if forgotten then ASSuME that this is an https server.
            instance_url = 'https://' + instance_url
        # also allow for shorthand cloud instances
        if '.' not in instance_url:
            instance_url = instance_url + '.jamacloud.com'
        return instance_url
    # otherwise the user did not specify this in the config. prompt the user for it now
    else:
        instance_url = input('Enter the Jama Instance URL:\n')
        credentials_object['instance url'] = instance_url
        return get_instance_url(credentials_object)


def get_username(credentials_object):
    if 'username' in credentials_object:
        username = str(credentials_object['username'])
        return username.strip()
    else:
        username = input('Enter the username (basic auth) or client ID (oAuth):\n')
        credentials_object['username'] = username
        return get_username(credentials_object)


def get_password(credentials_object):
    if 'password' in credentials_object:
        password = str(credentials_object['password'])
        return password.strip()
    else:
        password = getpass.getpass(prompt='Enter your password (basic auth) or client secret (oAuth):\n')
        credentials_object['password'] = password
        return get_password(credentials_object)


def get_project_id():
    try:
        return int(config['PARAMETERS']['project id'])
    except:
        print("missing project id... please provide a project id in the config ini")
        sys.exit()


def get_relationship_type():
    try:
        return int(config['PARAMETERS']['relationship type'])
    except:
        print("missing relationship type... please provide a relationship type id in the config ini")
        sys.exit()


def using_relationship_type():
    return 'relationship type' in config['PARAMETERS']


def get_oauth(credentials_object):
    if 'using oauth' in credentials_object:
        # this is user input here so lets be extra careful
        user_input = credentials_object['using oauth'].lower()
        user_input = user_input.strip()
        return user_input == 'true' or user_input == 'yes' or user_input == 'y'
    else:
        oauth = input('Using oAuth to authenticate?\n')
        credentials_object['using oauth'] = oauth
        return get_oauth(credentials_object)


if __name__ == '__main__':
    start_time = time.time()

    config = configparser.ConfigParser()
    config.read('config.ini')
    client = init_jama_client()

    project_id = get_project_id()

    # do work
    relationships = client.get_relationships(project_id)
    removal_list = []

    # so wew have any relationships here to process?
    if len(relationships) == 0:
        print("There are zero relationships in project ID:[" + str(project_id) + "]")
        sys.exit()

    print(str(len(relationships)) + ' relationship(s) in project ID:[' + str(project_id) + ']')

    # are we filtering this list by relationship type?
    if using_relationship_type():
        relationship_type = get_relationship_type()
        for relationship in relationships:
            # we have a match on the relationship type?
            if relationship.get('relationshipType') == relationship_type:
                removal_list.append(relationship)
        print(str(len(removal_list)) + '/' + str(
            len(relationships)) + ' relationships have relationship type id: [' + str(relationship_type) + ']')
    # lets remove them all then
    else:
        removal_list = relationships

    print("\nDeleting " + str(len(removal_list)) + " relationships...\n")
    with ChargingBar('Deleting Relationships... ', max=len(relationships), suffix='%(percent).1f%% - %(eta)ds') as bar:
        for relationship in relationships:
            relationship_id = relationship.get('id')
            client.delete_relationships(relationship_id)
            bar.next()
        bar.finish()

    elapsed_time = '%.2f' % (time.time() - start_time)
    print('total execution time: ' + elapsed_time + ' seconds')

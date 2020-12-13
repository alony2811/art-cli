import argparse
import requests
import json
from os import path
from consts import Consts


class Actions(object):
    def __init__(self,username='None',password='None',servername='None',new_username='None',new_password ='None', \
                 new_user_email='None', delete_username='None'):
        self.servername = servername
        self.username = username
        self.password = password
        self.token = ''
        self.new_username = new_username
        self.new_password = new_password
        self.new_user_email = new_user_email
        self.delete_username = delete_username

    def create_token(self):
        data = {Consts.USERNAME: self.username,Consts.SCOPE: Consts.API}
        r = requests.post(url=Consts.HTTPS+self.servername+Consts.API_SECURITY_TOKEN, data=data,\
                          auth=(self.username, self.password))
        r = json.loads(r.text)
        data ={}
        data[Consts.USERNAME]=self.username
        data[Consts.SERVERNAME]=self.servername
        data[Consts.ACCESS_TOKEN]=r[Consts.ACCESS_TOKEN]
        with open(Consts.TOKEN_FILE_NAME,'w') as token_file:
            json.dump(data, token_file)
        return


    def get_token_details(self):
        with open(Consts.TOKEN_FILE_NAME) as json_file:
            data = json.load(json_file)
            self.username = data[Consts.USERNAME]
            self.servername = data[Consts.SERVERNAME]
            self.token = data[Consts.ACCESS_TOKEN]

    def ping(self):
        if path.exists(Consts.TOKEN_FILE_NAME):
            self.get_token_details()
            r = requests.get(url=Consts.HTTPS+self.servername+Consts.API_PING)
            print(r.text)
        else:
            print('please login to your SaaS')
        return

    def version(self):
        if path.exists(Consts.TOKEN_FILE_NAME):
            self.get_token_details()
            r = requests.get(url=Consts.HTTPS+self.servername+Consts.API_VERSION, \
                             headers={'Authorization': 'Bearer '+str(self.token)})
            r = json.loads(r.text)
            print(r['version'])
        else:
            print('please login to your SaaS')
        return

    def create_user(self):
        if path.exists(Consts.TOKEN_FILE_NAME):
            self.get_token_details()
            data = json.dumps({Consts.NAME: self.new_username,Consts.PASSWORD: self.new_password, \
                               Consts.EMAIL: self.new_user_email})
            r = requests.put(url= Consts.HTTPS+self.servername+Consts.API_USERS+self.new_username, data = data, \
                             headers={'Authorization': 'Bearer '+str(self.token)})
            if r.status_code == 201:
                print('user created successfully!')
                return
            else:
                print(r.text)
            return
        else:
            print('please login to your SaaS')
        return

    def delete_user(self):
        if path.exists(Consts.TOKEN_FILE_NAME):
            self.get_token_details()
            r = requests.delete(url= Consts.HTTPS+self.servername+Consts.API_USERS+self.delete_username, \
                                headers={'Authorization': 'Bearer '+str(self.token)})
            if r.status_code == 200:
                print('user deleted successfully!')
                return
            else:
                print(r.text)
                return
        else:
            print('please login to your SaaS')
        return

    def get_storage_info(self):
        if path.exists(Consts.TOKEN_FILE_NAME):
            self.get_token_details()
            r = requests.get(url= Consts.HTTPS+self.servername+Consts.API_STORAGE_INFO, \
                             headers={'Authorization': 'Bearer '+str(self.token)})
            r = json.loads(r.text)
            print(json.dumps(r, indent=4, sort_keys=True))
            return
        else:
            print('please login to your SaaS')
        return

def main():
    parser = argparse.ArgumentParser(description='API CLI to manage an Artifactory SaaS instance', \
                                     epilog='Enjoy the program! :)')
    parser.add_argument('command', choices=['login','ping','version','create-user','delete-user','storage-info'], \
                        help='actions can be perform')
    parser.add_argument('-u','--username', type=str, default=None)
    parser.add_argument('-p','--password', type=str, default=None)
    parser.add_argument('-s','--servername', type=str, default=None, help='e.g. alony@jfrog.io')
    parser.add_argument('-nu','--newusername', type=str, default=None, help='new username')
    parser.add_argument('-np','--newpassword', type=str, default=None, help='password for the new username')
    parser.add_argument('-ne','--newuseremail', type=str, default=None,help='new username email')
    parser.add_argument('-du','--deleteusername', type=str, default=None,help='deleted username')
    args = parser.parse_args()

    if args.command == 'login':
        if args.username is None or args.password is None or args.servername is None:
            parser.error('--username, --password and --servername must be given together')
        else:
            action = Actions(username=args.username, password=args.password, servername= args.servername)
            action.create_token()

    if args.command == 'ping':
        action = Actions()
        action.ping()

    if args.command == 'version':
        action = Actions()
        action.version()

    if args.command == 'create-user':
        if args.newusername is None or args.newpassword is None or args.newuseremail is None:
            parser.error('--newusername, --newpassword and --newuseremail must be given together')
        else:
            action = Actions(new_username=args.newusername, new_password=args.newpassword, )
            action.create_user()

    if args.command == 'delete-user':
        if args.deleteusername is None:
            parser.error('--deleteusername must be given')
        else:
            action = Actions(delete_username=args.deleteusername)
            action.delete_user()

    if args.command == 'storage-info':
        action = Actions()
        action.get_storage_info()



if __name__ == '__main__':
    main()






















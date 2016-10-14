##############################################################################################
#    Copyright 2016 myKaarma (www.mykaarma.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################################################################

# Inspired by http://www.shiftedup.com/2014/11/13/how-to-bulk-remove-files-from-slack 
# and then additions by animeshpathak@mykaarma
# Fork us at https://github.com/mykaarma/slack-cleaner/


import requests
import json
import calendar
from datetime import datetime, timedelta

DEBUG_PRINT = False

_domain = "myslacksubdomain"
NUM_DAYS = 15

def delete_old_files(_token,u, num_days):
    """
    deletes all messages more than num_days old for user u. The object u should be a dict with params "id" for the internal ID and "name" for the slack username.
    """
    print "Deleting files older than %d days for user %s/%s..." % (num_days,u["name"],u["id"])
    count = 0
    while 1:
        files_list_url = 'https://slack.com/api/files.list'
        date = str(calendar.timegm((datetime.now() + timedelta(-num_days))
            .utctimetuple()))
        data = {"token": _token, "ts_to": date, "user":u["id"]}
        response = requests.post(files_list_url, data = data)
        if len(response.json()["files"]) == 0:
            break
        for f in response.json()["files"]:
            try:
                #The encoding to UTF-8 is needed for files with weird names.
                print "\tDeleting file %s (%s) ... " % (f["name"].encode("utf-8") , f["id"]),
            except Error:
                print "\tcannot decode filename, but I will delete something :) ...",
            timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
            delete_url = "https://" + _domain + ".slack.com/api/files.delete?t=" + timestamp
            response = requests.post(delete_url, data = {
                "token": _token, 
                "file": f["id"], 
                "set_active": "true", 
                "_attempts": "1"})
            if DEBUG_PRINT:
                print response
            print "success!"
            count = count + 1
    print "\tDONE! %d files deleted." % count
    return count

def list_all_users(_token):
    """
    returns the list of all users. The users are returned as dictionaries, and u["id"] and u ["name"] will give the ID (to be used in other API calls) and slack usernames.
    """
    user_list = [] #empty list
    print "Trying to get all users..."
    users_list_url = 'https://slack.com/api/users.list'
    data = {"token": _token}
    response = requests.post(users_list_url, data = data)
    if len(response.json()["members"]) == 0:
        print "no users found"
        return
    for u in response.json()["members"]:
        if DEBUG_PRINT:
            print "%s: %s " % (u["id"], u["name"])
        user_list.append({'id':u["id"],'name':u["name"]})
    if DEBUG_PRINT:
        print "user listing complete."
    return user_list
    
def usage():
    """
    prints usage
    """
    print "python slack-cleaner.py -t slacktoken [-n numdays] [-u username]"
    print "python slack-cleaner.py --token slacktoken [--num-days numdays] [--username user_name]"
    print "default num-days is %d, and by default it tries to delete files of all users" % NUM_DAYS
    
if __name__ == '__main__':
    import getopt, sys
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:n:u:", ["help", "token=","num-days=","username="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    token = None
    for o, a in opts:
        if DEBUG_PRINT:
            print "%s = %s" % (o,a)
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-t", "--token"):
            token = a
        elif o in ("-n", "--num-days"):
            NUM_DAYS = int(a)
        elif o in ("-u", "--username"):
            username = a
        else:
            assert False, "unhandled option"

    if not token:
        usage()
        sys.exit(-1)
            
    user_list = list_all_users(token)
    print "%d users found, proceeding to delete files older than % d days..." % (len(user_list),NUM_DAYS)
    total = 0
    for u in user_list:
        if (not username or u["name"] == username):
            print "Deleting files for %s: %s ..." % (u["id"], u["name"]),
            count = delete_old_files(token,u,NUM_DAYS)
            print "%d deleted!" % count
            total = total + count
    print "%d files deleted in total" % total

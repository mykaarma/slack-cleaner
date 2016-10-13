# slack-cleaner
A Python tool to delete old files from Slack. This tool, when used with an admin token, will delete _public_ files of _all_ users of a domain.

## Usage
1. Get a token from https://api.slack.com/docs/oauth-test-tokens/ 
2. Change the `_domain` variable from `myslacksubdomain` to your slack subdomain. E.g, if your URL is `mycompany.slack.com`, set `_domain` to `mycompany`
3. Be sure to have python, and also the requests library from http://docs.python-requests.org/en/latest/user/install/#install
4. Invoke the tool as
```
python slack-cleaner.py -t slacktoken [-n numdays]
``` 
or 
```
python slack-cleaner.py --token slacktoken [--num-days numdays]
```
(The default `num-days` is 30)

## License and Copyright
```
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
```
Inspired by http://www.shiftedup.com/2014/11/13/how-to-bulk-remove-files-from-slack and then additions by animeshpathak@mykaarma


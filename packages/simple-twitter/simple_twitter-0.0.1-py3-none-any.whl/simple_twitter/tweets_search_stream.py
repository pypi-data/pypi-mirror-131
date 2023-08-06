import datetime
import json
import os
import requests

from simple_twitter.exceptions import InvalidTokenException, InvalidRulesException, SameRulesValueException

class TweetsSearchStream:
    
    def __init__(self, token: str, rules: list):

        # validate token and set headers
        if str(token).strip() == '':
            raise InvalidTokenException()
        self._headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        # validate and set rules
        if len(rules) == 0:
            raise InvalidRulesException()
        self._rules_value = list()
        for rule in rules:
            if list(rule.keys()) != ['name','value']:
                raise InvalidRulesException()
            if (type(rule['name']) != str or type(rule['value']) != str or
                str(rule['name']).strip() == '' or str(rule['value']).strip() == ''):
                raise InvalidRulesException()
            if rule['value'] in self._rules_value:
                raise SameRulesValueException()
            self._rules_value.append(rule['value'])
        self._rules_name = rules

        # set api url
        self._api_url = 'https://api.twitter.com/2/tweets/search/stream'

    def _get_rules(self):
        resp = requests.get(
            headers=self._headers,
            url=self._api_url+'/rules'
        )
        resp.raise_for_status()
        return resp.json()['data']

    def _post_rules(self, data):
        return requests.post(
            headers=self._headers,
            url=self._api_url+'/rules',
            data=json.dumps(data)
        )

    def _get_stream(self):
        return requests.get(
            headers=self._headers,
            url=self._api_url,
            stream=True
        )

    def start(self):

        # RULES ================================================================

        rules_add = []
        rules_value = []
        rules_delete = []

        # get
        for rule in self._get_rules():
            if rule['value'] not in self._rules_value:
                rules_delete.append(rule['id'])
            else:
                rules_value.append(rule['value'])

        # delete
        if len(rules_delete) > 0:
            resp = self._post_rules({'delete':{'ids':rules_delete}})
            print(f'DELETE STREAM RULES: {resp.text}')

        # add
        for value in self._rules_value:
            if value not in rules_value:
                rules_add.append({'value':value})
        if len(rules_add) > 0:
            resp = self._post_rules({'add':rules_add})
            print(f'ADD STREAM RULES: {resp.text}')

        # base
        self._rules = dict()
        for rule in self._get_rules():
            rule_value = rule['value']
            rule_name = [r['name'] for r in self._rules_name if r['value'] == rule_value][0]
            self._rules[rule['id']] = {
                'name': rule_name,
                'value': rule_value
            }

        # STREAM ===============================================================

        for line in self._get_stream().iter_lines():
            if not line:
                continue

            payload = json.loads(line)
            for rule in payload['matching_rules']:
                rule_id = rule['id']
                rule = self._rules[rule_id]
                yield {
                    'dt_utc': datetime.datetime.utcnow().isoformat(),
                    'tweet_id': payload['data']['id'],
                    'tweet_text': payload['data']['text'],
                    'rule_id': rule_id,
                    'rule_name': rule['name'],
                    'rule_value': rule['value'],
                }

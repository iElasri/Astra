#!/usr/bin/env python
import requests


class GetSMSCode:
    def __init__(self, config):
        self.apikey = config['sms-activate.ru']['apikey']
        self.api_url = config['sms-activate.ru']['api_url']

    @property
    def getBalance(self):
        # working on new
        payload = {
            'action': 'getBalance',
            'api_key': self.apikey,
        }
        r = requests.post(self.api_url, params=payload)
        r.encoding = 'utf-8'

        balance = r.text.split(':')[1]
        return balance

    def getStatus(self, order_id):
        '''
                STATUS_CANCEL - Order cancelled
                STATUS_WAIT_READY - Wait ready
                STATUS_WAIT_CODE - Wait sms and code
                STATUS_OK:$CODE - Code received
                STATUS_WAIT_RETRY - Wait code retry1
                STATUS_WAIT_SCREEN - Wait code retry2
                STATUS_WAIT_RESEND - Wait sms resend
                STATUS_ACCESS:$CODE - Order finished
                STATUS_ACCESS_SCREEN:$CODE - Order finished
                STATUS_ERROR_NUMBER - Error with phone number
                STATUS_ERROR - the activator Error
        '''
        # api_key = YOUR_API_KEY
        # action = getStatus
        # id = ORDER_ID

        payload = {
            'action': 'getStatus',
            'api_key': self.apikey,
            'id': order_id
        }

        r = requests.post(self.api_url, params=payload)
        r.encoding = 'utf-8'
        response = r.text

        data = {'status': response, 'code': ''}

        if ':' in response:
            data['status'] = response.split(':', 1)[0]
            data['code'] = response.split(':', 1)[1]

        return data

    def setStatus(self, order_id, status):
        # api_key = YOUR_API_KEY
        # action = setStatus
        # id = ORDER_ID
        # status = SET_STATUS

        payload = {
            'api_key': self.apikey,
            'action': 'setStatus',
            'id': order_id,
            'status': status
        }

        r = requests.post(self.api_url, params=payload)
        r.encoding = 'utf-8'

        return r.text

    def get_mobile_number(self):
        '''
            gets the number but does not buy it until you set status
        '''
        # api_key = Your_api_key
        # action = getNumber
        # country = COUNTRY_AND_OPERATOR
        # service = PRODUCT
        # count = TOTAL_SMS_NUMBER

        pn = 1
        while pn:
            payload = {
                'api_key': self.apikey,
                'action': 'getNumber',
                'service': 'tg',
                'country': '37',
                'count': '1'
            }

            r = requests.post(self.api_url, params=payload)
            r.encoding = 'utf-8'
            response = r.text

            if response != 'NO_NUMBERS':
                return response.split(':')[1], response.split(':')[2]
            else:
                print('NO-NUMBER')

    def blacklist(self, mobile_number):
        payload = {
            'action': 'addblack',
            'username': self.username,
            'api_key': self.apikey,
            'pid': 10,
            'mobile': mobile_number,
        }
        r = requests.post(self.api_url, params=payload)
        r.encoding = 'utf-8'
        if r.text == 'Message|Had add black list':
            return '{} has been blacklisted.'.format(mobile_number)

    @property
    def mobile_list(self):
        payload = {
            'action': 'mobilelist',
            'username': self.username,
            'api_key': self.apikey,
        }
        r = requests.post(self.api_url, params=payload)
        r.encoding = 'utf-8'
        mobile_list = []
        for mobile in r.text.split(','):
            keys = ['mobile', 'pid']
            values = mobile.split('|')
            mobile_list.append(dict(zip(keys, values)))
        return mobile_list

    def get_code(self, mobile_number):
        payload = {
            'action': 'getsms',
            'username': self.username,
            'api_key': self.apikey,
            'pid': 10,
            'mobile': mobile_number,
            'author': self.username,
        }
        r = requests.post(self.api_url, params=payload)
        r.encoding = 'utf-8'
        code = ''.join([num for num in list(
            r.text.split('|')[1]) if num.isdigit()])
        return code

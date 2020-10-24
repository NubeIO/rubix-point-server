# import requests
# import json
#
# authorization_code = "api:122222:1111112:LA5"
# members = [12345,1234567]
# for member in members:
#     url = "http://api.example.com/v1.14/member?id="+str(member)
#
#     response = requests.get(url, headers=header)
#
#     member_check = json.loads(response.text)
#     final_member_status = member_check["response"]["member"]["is_expired"]
#
#     print str(member) + " expired status: " + str(final_member_status)
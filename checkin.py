import requests, json, os

# server酱开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
sever = os.environ["SERVE"]
# 填写server酱sckey,不开启server酱则不用填
sckey = os.environ["SCKEY"]
# 填入glados账号对应cookie
cookie = os.environ["COOKIE"]


def start():
    checkin_url = 'https://glados.rocks/api/user/checkin'
    status_url = 'https://glados.rocks/api/user/status'
    referer_url = 'https://glados.rocks/console/checkin'

    # 发起签到请求
    checkin = requests.post(checkin_url, headers={'cookie': cookie, 'referer': referer_url})
    # 获取剩余天数
    state = requests.get(status_url, headers={'cookie': cookie, 'referer': referer_url})

    if 'message' in checkin.text:
        # 获取请求日志
        message = checkin.json()['message']
        # 获取剩余天数
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        print("本次签到信息: %s , 剩余使用天数: %s" % (message, time))
        if sever == 'on':
            requests.get('https://sc.ftqq.com/' + sckey + '.send?text=' + message + '，you have ' + time + ' days left')
    else:
        requests.get('https://sc.ftqq.com/' + sckey + '.send?text=cookie过期')
        print("cookie已过期，请更换cookie信息")


def main_handler(event, context):
  return start()


if __name__ == '__main__':
    start()

import os
import sys
import datetime
import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2025-01-01",  # 신정
    "2025-03-01",  # 삼일절
    "2025-05-05",  # 어린이날
    "2025-05-06",  # 대체공휴일
    "2025-06-06",  # 현충일
    "2025-08-15",  # 광복절
    "2025-10-03",  # 개천절
    "2025-10-06",  # 추석
    "2025-10-07",  # 추석연휴
    "2025-10-08",  # 대체공휴일
    "2025-10-09",  # 한글날
    "2025-12-25",  # 크리스마스
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f":loudspeaker: *『인사총무팀 공지』* \n\n"

        notice_msg = (
            f"안녕하세요? 평택 클러스터 구성원 여러분! 인사총무팀 입니다. :blush:\n"
            f"\n"
            f" *시설안전이슈* 채널 이용에 대해 아래와 같이 공지 드리오니 협조 부탁드리겠습니다.\n\n"
            f"\n"
            f":체크1: *<시설안전 이슈 채널 이용 시 협조 사항>*\n\n"
            f":one: *필수 내용* : A/S요청 , 보수요청, 확인필요 (AS,보수,확인 가능)\n"
            f":two: *장소 설명* : 최대한 각 층 오버헤드도어 (OHD) 및 방열도어 (챔버) 번호로 설명\n"
            f":three: *증상 설명* : 원인불명 또는 작동불능, 확인필요로 하는 사항에 대해서 기재\n"
            f"\n\n"
            f":alert: *<중요사항>* :alert: \n"
            f"> 현장에서 주로 사용하시는 포장대번호, 지번, 설비번호로 장소 설명 시 *현장 확인이 지연될 수 있습니다.*\n"
            f"\n\n"
            f"📌 시설물 파손,임시보수요청,A/S요청 등 해당 사항에 대해서만 본 채널에 공유 바랍니다.\n"
            f"📌 그 외 내용에 대해서는 <#C05NVF8AQPL|12_문의사항_평택> 채널 이용 바랍니다.\n"
            f"\n\n"
            f":slack: *<문의사항>* :*<@U05NXEAL43E> <@U04RT8X7D9N> <@U07QC9WQ8JX>*\n\n"
            f"감사합니다.\n"
       )
 
        # 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()

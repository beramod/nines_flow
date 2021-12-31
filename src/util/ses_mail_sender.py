import boto3
from botocore.exceptions import ClientError

class SESMailSender:
    def __init__(self):
        self._from = 'noti@soulenergy.co.kr'  # 보내는사람 고정
        self._recipient = []  # 받는사람
        self._aws_region = "ap-northeast-2"  # 지역코드
        self._charset = "UTF-8"  # 인코딩 정보
        self._client = None
        self.connect()

    def connect(self):
        client = boto3.client('ses', region_name=self._aws_region)
        self._client = client

    def send(self, to, subject, body_text, body_html):
        try:
            response = self._client.send_email(
                Destination={
                    'ToAddresses': to
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self._charset,
                            'Data': body_html,
                        },
                        'Text': {
                            'Charset': self._charset,
                            'Data': body_text,
                        },
                    },
                    'Subject': {
                        'Charset': self._charset,
                        'Data': subject,
                    },
                },
                Source=self._from,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
from django.conf import settings
from django.template.loader import get_template
from boto3.session import Session

TEMPLATE_BASE = 'restaurants/email/'


def _get_template(template_name, context):
    return get_template(TEMPLATE_BASE + template_name).render(context)


class EmailSender:
    @staticmethod
    def send_email(to_email, from_email, context, subject_template_name,
                   plain_body_template_name, html_body_template_name=None):
        raise NotImplementedError("Not implemented in the base class")


class MockEmailSender(EmailSender):
    sentEmails = []

    @staticmethod
    def send_email(to_email, from_email, context, subject_template_name,
                   plain_body_template_name, html_body_template_name=None):
        email = Email(to_email, from_email,
                      _get_template(subject_template_name, context).strip(),
                      _get_template(plain_body_template_name, context))
        MockEmailSender.sentEmails.append(email)
        email.print()


class Email():
    def __init__(self, to_email, from_email, subject, body):
        self.to_email = to_email
        self.from_email = from_email
        self.subject = subject
        self.body = body

    def print(self):
        print('Mock email to ' + self.to_email + ' from ' + self.from_email)
        print('Subject: ' + self.subject)
        print('Body: ' + self.body)


class SESEmailSender(EmailSender):

    @staticmethod
    def send_email(to_email, from_email, context, subject_template_name,
                   plain_body_template_name, html_body_template_name=None):
        subject = _get_template(subject_template_name, context).strip()
        body = _get_template(plain_body_template_name, context)
        SESUtil().send_email(to_email, from_email, subject, body)


class SESUtil:
    def send_email(self, to_email, from_email, subject, body):
        session = Session(settings.AWS_ACCESS_KEY,
                          settings.AWS_SECRET_ACCESS_KEY,
                          region_name='eu-west-1')
        client = session.client('ses')
        return client.send_email(
                Source=from_email,
                Destination=self._destination(to_email),
                Message=self._message(subject, body),
        )

    @staticmethod
    def _destination(to_email):
        return {
            'ToAddresses': [
                to_email,
            ],
            'CcAddresses': [],
            'BccAddresses': []
        }

    @staticmethod
    def _message(subject, body):
        return {
            'Subject': {
                'Data': subject,
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': body,
                    'Charset': 'utf-8'
                }
            }
        }

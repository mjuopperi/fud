from django.conf import settings
from django.template.loader import get_template
from boto3.session import Session

ACTIVATION_SUBJECT_TEMPLATE = 'restaurants/email/activation_email_subject.txt'
ACTIVATION_BODY_TEMPLATE = 'restaurants/email/activation_email_body.txt'


class EmailSender:
    @staticmethod
    def send_email(to_email, from_email, context, subject_template_name=None,
                   plain_body_template_name=None, html_body_template_name=None):
        raise NotImplementedError("Not implemented in the base class")


class MockEmailSender(EmailSender):
    @staticmethod
    def send_email(to_email, from_email, context, subject_template_name=None,
                   plain_body_template_name=None, html_body_template_name=None):
        print('Mock email to ' + to_email + ' from ' + from_email)
        print('Subject: ' + get_template(ACTIVATION_SUBJECT_TEMPLATE).render(context))
        print('Body: ' + get_template(ACTIVATION_BODY_TEMPLATE).render(context))


class SESEmailSender(EmailSender):

    @staticmethod
    def send_email(to_email, from_email, context, subject_template_name=None,
                   plain_body_template_name=None, html_body_template_name=None):
        subject = get_template(ACTIVATION_SUBJECT_TEMPLATE).render(context).strip()
        body = get_template(ACTIVATION_BODY_TEMPLATE).render(context)
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

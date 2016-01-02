from django.template.loader import get_template

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

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

from market.settings import FROM_EMAIL,EMAIL_ADMIN
from emails.models import EmailSendingFact, EmailType
from django.forms.models import model_to_dict


class SendingEmail(object):
    from_email = "Интернет магазин запчастей Вираж<%s>" % FROM_EMAIL
    reply_to_emails = [from_email]
    target_emails = []
    bcc_emails = []


    def sending_email(self,type_id,email=None,order=None,password=None):
        if not email:
            email = EMAIL_ADMIN

        target_emails = [email]


        vars= dict()

        if type_id==1:
            subject = 'Новый заказ'
            vars["order_fields"] = model_to_dict(order)
            vars["order"] = order
            vars["products_in_order"] = order.productinorder_set.filter(is_active=True)
            message = get_template('emails_templates/order_notification_admin.html').render(vars)

        elif type_id==2:
            subject = "От Вас поступил новый заказ"
            vars["order"] = order
            message = get_template('emails_templates/order_notification_customer.html').render(vars)
        elif type_id==3:
            subject = "Регистрация"
            vars["user"]= email
            vars["password"]=password
            print('type 3')
            message = get_template('emails_templates/registered.html').render(vars)
        elif type_id==4:
            subject = "Смена пароля"
            vars["user"]= email
            vars["password"]=password
            print('type 3')
            message = get_template('emails_templates/change_password.html').render(vars)
        elif type_id==5:
            subject = "Сброс пароля"
            vars["user"]= email
            vars["password"]=password
            print('type 3')
            message = get_template('emails_templates/lost_password.html').render(vars)

        msg = EmailMessage(
            subject,message,from_email=self.from_email,
            to=target_emails,bcc=self.bcc_emails,reply_to=self.reply_to_emails,
        )
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()

        kwargs = {
            "type":type_id,
            "email":email
        }
        if order:
            kwargs["order"] = order

        print('Email was sent secsecfull')


from odoo.addons.base.models.ir_mail_server import IrMailServer
from odoo.addons.mail.models.mail_message import Message
from odoo import api


def post_load_hook():
    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   smtp_session=None):
        """Sends an email directly (no queuing).

        No retries are done, the caller should handle MailDeliveryException in order to ensure that
        the mail is never lost.

        If the mail_server_id is provided, sends using this mail server, ignoring other smtp_* arguments.
        If mail_server_id is None and smtp_server is None, use the default mail server (highest priority).
        If mail_server_id is None and smtp_server is not None, use the provided smtp_* arguments.
        If both mail_server_id and smtp_server are None, look for an 'smtp_server' value in server config,
        and fails if not found.

        :param message: the email.message.Message to send. The envelope sender will be extracted from the
                        ``Return-Path`` (if present), or will be set to the default bounce address.
                        The envelope recipients will be extracted from the combined list of ``To``,
                        ``CC`` and ``BCC`` headers.
        :param smtp_session: optional pre-established SMTP session. When provided,
                             overrides `mail_server_id` and all the `smtp_*` parameters.
                             Passing the matching `mail_server_id` may yield better debugging/log
                             messages. The caller is in charge of disconnecting the session.
        :param mail_server_id: optional id of ir.mail_server to use for sending. overrides other smtp_* arguments.
        :param smtp_server: optional hostname of SMTP server to use
        :param smtp_encryption: optional TLS mode, one of 'none', 'starttls' or 'ssl' (see ir.mail_server fields for explanation)
        :param smtp_port: optional SMTP port, if mail_server_id is not passed
        :param smtp_user: optional SMTP user, if mail_server_id is not passed
        :param smtp_password: optional SMTP password to use, if mail_server_id is not passed
        :param smtp_debug: optional SMTP debug flag, if mail_server_id is not passed
        :return: the Message-ID of the message that was just sent, if successfully sent, otherwise raises
                 MailDeliveryException and logs root cause.
        """
        smtp_from = (
            self.sudo().env['ir.config_parameter'].get_param('mail_force_sender.sender_email_address')
        )
        email_to = message['To']
        email_cc = message['Cc']
        email_bcc = message['Bcc']
        del message['Bcc']

        smtp_to_list = [
            address
            for base in [email_to, email_cc, email_bcc]
            for address in extract_rfc2822_addresses(base)
            if address
        ]
        assert smtp_to_list, self.NO_VALID_RECIPIENT

        x_forge_to = message['X-Forge-To']
        if x_forge_to:
            # `To:` header forged, e.g. for posting on mail.channels, to avoid confusion
            del message['X-Forge-To']
            del message['To']           # avoid multiple To: headers!
            message['To'] = x_forge_to

        # Do not actually send emails in testing mode!
        if getattr(threading.currentThread(), 'testing', False) or self.env.registry.in_test_mode():
            _test_logger.info("skip sending email in test mode")
            return message['Message-Id']

        try:
            message_id = message['Message-Id']
            smtp = smtp_session
            smtp = smtp or self.connect(
                smtp_server, smtp_port, smtp_user, smtp_password,
                smtp_encryption, smtp_debug, mail_server_id=mail_server_id)
            smtp.sendmail(smtp_from, smtp_to_list, message.as_string())
               # do not quit() a pre-established smtp_session
            if not smtp_session:
                smtp.quit()
        except smtplib.SMTPServerDisconnected:
            raise
        except Exception as e:
            params = (ustr(smtp_server), e.__class__.__name__, ustr(e))
            msg = _("Mail delivery failed via SMTP server '%s'.\n%s: %s") % params
            _logger.info(msg)
            raise MailDeliveryException(_("Mail Delivery Failed"), msg)
        return message_id

    if not hasattr(IrMailServer, 'send_email_original'):
        IrMailServer.send_email_original = IrMailServer.send_email
        IrMailServer.send_email = send_email

    @api.model
    def _get_default_from(self):
        return (
            self.sudo().env['ir.config_parameter'].get_param('mail_force_sender.sender_email_address')
        )

    if not hasattr(Message, '_get_default_from_original'):
        Message._get_default_from_original = Message._get_default_from
        Message._get_default_from = _get_default_from

# C:\BookTour\webapp\travella\domains\services\access_log_service.py

from dataclasses import dataclass
import uuid
from travella.domains.models.log_models import AccessLog


def save_log(form:'AccessLogForm', account_id:uuid) -> int:
    """
    Saves an AccessLog entry, ensuring the form has a valid access type.
    """
    if not form.access_type:
        # If the access type is not provided, raise a ValueError to debug the source
        raise ValueError("Cannot save AccessLog: 'access_type' is required.")

    log = form.get_model(account_id)
    log.save()
    return log.id

@dataclass
class AccessLogForm:
    access_type:AccessLog.Type
    status:AccessLog.Status
    message:str

    @staticmethod
    def sign_in_success_form() -> 'AccessLogForm':
        return AccessLogForm(
            access_type=AccessLog.Type.SIGN_IN,
            status=AccessLog.Status.SUCCESS,
            message='Sign In Success'
        )
    
    @staticmethod
    def sign_out_success_form() -> 'AccessLogForm':
        return AccessLogForm(
            access_type=AccessLog.Type.SIGN_OUT,
            status=AccessLog.Status.SUCCESS,
            message='Sign Out Sccess'
        )
    
    @staticmethod
    def wrong_password_form(password:str) -> 'AccessLogForm':
        return AccessLogForm(
            access_type=AccessLog.Type.SIGN_IN,
            status=AccessLog.Status.FAIL,
            message=f'Wrong Password : {password}'
        )

    def get_model(self, account_id:uuid) -> AccessLog:
        return AccessLog(
            access_type = self.access_type,
            status = self.status,
            message = self.message,
            account_id = account_id,
        )
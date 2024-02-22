from .models import Referral, TelegramUser


def register_user(user_id: str, user_role: int = 2) -> tuple[int, bool]:
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if not user:
        TelegramUser.objects.create(chat_id=user_id, role=user_role)
        return user_role, False
    else:
        return user.role, True


def set_state(user_id: str, state: str):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user:
        user.state = state
        user.save()


def set_user_data(user_id: str, field: str, value: str):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if hasattr(user, field):
        setattr(user, field, value)
        user.save()


def create_referal(user_id, refered_user_id):
    Referral.objects.create(
        referer__chat_id=refered_user_id, referred_user__chat_id=user_id
    )

import logging
from django.contrib.auth.mixins import UserPassesTestMixin

# ユーザ認証済みかスーパーユーザの場合
class YouOrSuperMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


# スーパーユーザの場合
class OnlySuperMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_superuser


# サービス用ロギングデコレータ
def log_service(svc_name):
    logger = logging.getLogger('root')
    def _log_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info('{}の処理を開始します'.format(svc_name))
                return func(*args, **kwargs)

            except Exception as e:
                logger.error('エラーが発生しました。{}'.format(str(e)))
                raise e

            finally:
                logger.info('{}の処理を終了します'.format(svc_name))

        return wrapper

    return _log_decorator
from celery import task


@task(bind=True, default_retry_delay=3, max_retries=5)
def migrate(self):
    """

    :param bind: 与task实例绑定，所以此函数就是一个成员函数，需传入self.
    :param default_retry_delay: 默认重新执行间隔.
    :param max_retries: 最多重新执行次数，防止无限执行.
    :return:
    """
    try:
        # do_something()
        pass
    except Exception as e:
        self.retry(exc=e)

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if not self.request.user.is_authenticated:
            context['user_is_login'] = False
        else:
            context['user_is_login'] = True
        return context
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    """Cобственный класс для формы регистрации."""

    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        # email обязательно заполнять
        self.fields["email"].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {"username": UsernameField}

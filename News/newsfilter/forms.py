from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, NewsCategory


class CreateUserForm(UserCreationForm):
    categories = NewsCategory.objects.all()
    category_choices = []

    for each in categories:
        category_choices.append((each.id, each.name))
    b = tuple(category_choices)

    subscribe_to = forms.MultipleChoiceField(choices=b)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'subscribe_to',
            'password1',
            'password2',
        )


# class EditUserForm(UserChangeForm):
#     categories = NewsCategory.objects.all()
#     category_choices = []

#     for i, each in enumerate(categories):
#         category_choices.append((i+1, each.name))

#     subscribe_to = forms.MultipleChoiceField(choices=category_choices)

#     class Meta:
#         model = User
#         fields = (
#             'first_name',
#             'last_name',
#             'email',
#             'subscribe_to'
#             'password',
#         )

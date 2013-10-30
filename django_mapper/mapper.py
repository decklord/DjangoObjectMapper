from social.models import User, Source, UserToken
from django.db import connection, transaction

class Mapper(object):

    def __init__(self, entity):
        'Sets the initial entity that we want to transform and save into a Django object'
        self.external_object = entity
        self.set_base_data()

    def set_base_data(self):
        pass

    def get_or_create_django_object(self, object_class, params):

        try:
            self.django_object, created = object_class.objects.select_for_update().get_or_create(
                **params
            )
            transaction.commit()
        except Exception:
            connection._rollback()
            self.django_object = object_class.objects.get(pk = params['pk'])
            created = False

        if not created:
            self.django_object = self.update(params['defaults'])

        return self.django_object, created

    def update_django_object(self, attributes):

        if not attributes:
            return self.django_object

        for key, val in attributes.items():
            setattr(self.django_object, key, val)

        self.django_object.save()
        return self.django_object

    def get_external_val(self, value, default = ''):

        try:
            val = getattr(self.external_object, value)
        except AttributeError:
            val = self.external_object.get(value, default)

        return val if val is not None else default

class TwitterMapper(Mapper):

    def set_base_data(self):

        self.source, _ = Source.objects.get_or_create(
            name = 'Twitter',
            defaults = {
                'url': 'http://www.twitter.com'
            }
        )

class TwitterUserMapper(TwitterMapper):

    def get_or_create(self):

        params = {
            "pk": self.get_external_val('id'),
            "defaults" : {

                'username': self.get_external_val('screen_name'),
                'fullname': self.get_external_val('name'),
                'url': "%s/%s" % (self.source.url, self.get_external_val('screen_name')),
                'source__id': self.source.pk,

                'information': self.get_external_val('description'),
                'location': self.get_external_val('location'),
                'time_zone': self.get_external_val('time_zone'),
                'website': self.get_external_val('url'),

                'nbr_statuses': self.get_external_val('statuses_count', 0),
                'nbr_friends': self.get_external_val('friends_count', 0),
                'nbr_followers': self.get_external_val('followers_count', 0),
                'nbr_favorites': self.get_external_val('favourites_count', 0)

            }
        }

        self.user, created = self.get_or_create_django_object(User, params)
        return self.user, created

    def set_token(self, token):

        params = {
            "user_id" : self.user.pk,
            "defaults" : {
                "access_token" : token
            }
        }

        self.user.tokens, created = self.get_or_create_django_object(UserToken, params)
        return self.user.tokens, created

    def set_profile_image(self):
        pass

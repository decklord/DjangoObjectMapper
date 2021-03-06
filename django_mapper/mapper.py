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
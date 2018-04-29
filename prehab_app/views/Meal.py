from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab_app.models.Meal import Meal
from prehab.permissions import Permission
from prehab_app.serializers.Meal import MealSerializer


class MealViewSet(GenericViewSet):

    def list(self, request):
        queryset = self.paginate_queryset(Meal.objects.all())
        data = MealSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            meal = Meal.objects.get(pk=pk)

        except Meal.DoesNotExist:
            return HTTP.response(404, 'Meal with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        data = MealSerializer(meal, many=False).data
        return HTTP.response(200, '', data)

    @staticmethod
    def create(request):
        try:
            if not Permission.verify(request, ['Admin']):
                raise HttpException(401)

            data = request.data
            # 1. Check schema
            SchemaValidator.validate_obj_structure(data, 'meal/create.json')

            # 2. Check if meal type is available
            if not any( data['meal_type_id'] in meal_type for meal_type in Meal.meal_types):
                raise HttpException(400, 'Meal Type does not exist.')

            new_meal = Meal(
                title=data['title'],
                description=data.get('description', None),
                multimedia_link=data.get('multimedia_link', None),
                meal_type=data['meal_type_id']
            )
            new_meal.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        data = {
            'meal_id': new_meal.id
        }
        return HTTP.response(201, '', data)

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')

import json
import uuid

from django.http import HttpResponse
from django.views.generic import View
from django.core import serializers
from .models import UserProxy

# TODO endpoints for remote UserProxy management

# class RestUserProxyView(View):
#
#     @staticmethod
#     def _get_user_proxy(key):
#         # Try to retrieve from pk
#         user_proxy = UserProxy.objects.filter(pk=key)
#         if user_proxy.exists():
#             return user_proxy.first()
#
#         # Try to retrieve from UUID
#         try:
#             uuid_user_id = uuid.UUID(key)
#         except ValueError | TypeError:
#             raise KeyError
#
#         user_proxy = UserProxy.objects.filter(user_id=uuid_user_id)
#
#         if user_proxy.exists():
#             return user_proxy.first()
#
#         # Doesn't exist
#         raise KeyError
#
#     def get(self, request, *args, **kwargs):
#
#         try:
#             user_proxy = self._get_user_proxy(kwargs["pk"])
#         except KeyError:
#             return HttpResponse(
#                 "UserProxy not found",
#                 status=404
#             )
#
#         response = serializers.serialize("json", [user_proxy])
#         return HttpResponse(response, status=200)
#
#     def post(self, request, *args, **kwargs):
#         incoming_data = json.loads(request.body)
#
#         remote_user_id = uuid.UUID(incoming_data["user_id"])
#
#         user_proxy = UserProxy(
#             user_id=remote_user_id
#         )
#
#         user_proxy.save()
#
#         response = serializers.serialize("json", [user_proxy])
#         return HttpResponse(response, status=201)
#
#     def patch(self, request, *args, **kwargs):
#         return self.put(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         incoming_data = json.loads(request.body)
#
#         try:
#             if "pk" in kwargs:
#                 user_proxy = self._get_user_proxy(kwargs["pk"])
#             else:
#                 user_proxy = self._get_user_proxy(incoming_data["user_id"])
#         except KeyError:
#             return HttpResponse(
#                 "UserProxy not found",
#                 status=404
#             )
#
#         user_proxy.user_id = incoming_data["user_id"]
#         user_proxy.save()
#
#         return HttpResponse(status=204)
#
#     def delete(self, request, *args, **kwargs):
#         try:
#             user_proxy = self._get_user_proxy(kwargs["pk"])
#         except KeyError:
#             return HttpResponse(
#                 "UserProxy not found",
#                 status=404
#             )
#
#         user_proxy.delete()
#         return HttpResponse(status=204)

from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q, Case, When
from rest_framework_extensions.cache.decorators import cache_response

from utils.response import APIResponse

from game import models as game_models


class IndexPageView(APIView):
    pass

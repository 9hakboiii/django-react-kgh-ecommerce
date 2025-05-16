from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.


# dev_28
# def hello_world(request):
#     response_data = {}
#     response_data["hello"] = "hello"
#     response_data["world"] = "world"

#     return HttpResponse(json.dumps(response_data))


# def hello_world_json(request):

#     response_data = {}
#     response_data["error"] = "error"
#     response_data["details"] = "헬로월드 에러입니다."

#     return JsonResponse(response_data, status=400)


# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# @api_view(["GET"])
# def hello_world_drf(request):
#     return Response({"message": "Hello World!"}) # 테스트용 템플릿도 포함됨

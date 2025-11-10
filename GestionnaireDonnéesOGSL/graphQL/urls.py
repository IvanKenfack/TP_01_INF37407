from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
<<<<<<< HEAD
    path('', csrf_exempt(GraphQLView.as_view(graphiql=True))),
=======
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
>>>>>>> be1f1f51ab058fac5059f89e68eba8b3149333f5
]
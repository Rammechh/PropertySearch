from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from projects.models import Project, Review
from .serializers import ProjectSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET' : '/api/projects'},
        {'GET' : '/api/projects/1'},
        {'POST' : '/api/projects/id/vote'},
        {'POST' : '/api/users/token'},
        {'POST' : '/api/users/token/refresh'}
    ]

    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id = pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id = pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )
    #review.value = up/down vote, we are passsing only {"value" : "up"} in postman. url projects/<str:pk>/vote/
    review.value = data['value']
    review.save()
    # used @property for getVoteCount so need o trigger as normal fn
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
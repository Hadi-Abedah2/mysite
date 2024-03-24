from rest_framework import viewsets
from ads.models import Ad, Comment
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .filters import AdFilter
from .serializers import AdSerializer, CommentSerializer, AdDetailSerializer, CommentDetailSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at') 
    serializer_class = AdSerializer
    filterset_class = AdFilter

    def get_serializer_class(self): 
        # Use the DetailedPostSerializer for the "retrieve" action
        if self.action == 'retrieve':
            # When accessing a specific object, use the DetailedPostSerializer
            return AdDetailSerializer
        # For other actions, use the default serializer class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        #return super().perform_create(serializer)

    @action(detail=True, methods=['get'], url_path='comments')
    def comments(self, request, pk=None):
        ad = get_object_or_404(Ad.objects.prefetch_related('comment_set'), pk=pk)
        comments = ad.comment_set.all() # will not hit the DB.
        serializer = CommentSerializer(comments, many=True)  
        return Response(serializer.data)

    @action(methods=[ 'get' ], detail=False, name='My Ads', url_path='my-ads')
    def my_ads(self, request):
        if request.user.is_authenticated:
            ads = Ad.objects.filter(owner=request.user).order_by('-created_at')
            serializer = AdSerializer(ads, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'sign in to see your ads'}, status=401)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at') 
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CommentDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    @action(methods=[ 'get' ], detail=False, name ='My Comments')
    def my_comments(self, request):
        if request.user.is_authenticated:
            comments = Comment.objects.filter(owner=request.user).order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'sign in to see your comments'}, status=401)
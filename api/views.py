from rest_framework.permissions import IsAuthenticated
from api.serializers import BookReviewSerializer
from books.models import BookReview
from rest_framework import viewsets

class BookReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')
    lookup_field = 'id'


# class BookReviewAPIView(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(book_review)
#
#         return Response(data=serializer.data)
#
#     def delete(self, reqeust, id):
#         book_review = BookReview.objects.get(id=id)
#         book_review.delete()
#
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class BookReviewListAPIView(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#         book_reviews = BookReview.objects.all().order_by('-created_at')
#         paginator = PageNumberPagination()
#         page_obj = paginator.paginate_queryset(book_reviews, request)
#         serializer = BookReviewSerializer(page_obj, many=True)
#
#         return paginator.get_paginated_response(serializer.data)
#
#
#     def post(self, request):
#         serializer = BookReviewSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

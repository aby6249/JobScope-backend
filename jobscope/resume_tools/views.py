from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import ResumeTool, ResumeToolReview, ResumeToolReaction
from .serializers import ResumeToolSerializer, ResumeToolReviewSerializer, ResumeToolReactionSerializer
from dashboard.models import UserActivity



class ResumeToolListView(APIView):

    def get(self, request):

        tools = ResumeTool.objects.annotate(
            avg_rating=Avg("reviews__rating")
        )

        data = []

        for tool in tools:

            good_count = tool.reactions.filter(reaction="good").count()
            bad_count = tool.reactions.filter(reaction="bad").count()

            data.append({
                "id": tool.id,
                "name": tool.name,
                "website_url": tool.website_url,
                "description": tool.description,
                "logo": tool.logo.url if tool.logo else None,
                "average_rating": round(tool.avg_rating or 0, 1),
                "total_reviews": tool.reviews.count(),
                "good_count": good_count,
                "bad_count": bad_count
            })

        return Response(data)
    


class ResumeToolDetailView(APIView):

    def get(self, request, pk):

        tool = ResumeTool.objects.get(id=pk)

        UserActivity.objects.create(

            user=request.user,

             activity_type="resume",

            object_id=tool.id

        )

        avg_rating = tool.reviews.aggregate(avg=Avg("rating"))["avg"]

        reviews = ResumeToolReview.objects.filter(tool=tool)

        good_count = tool.reactions.filter(reaction="good").count()
        bad_count = tool.reactions.filter(reaction="bad").count()

        return Response({
            "tool": {
                "id": tool.id,
                "name": tool.name,
                "website_url": tool.website_url,
                "description": tool.description,
                "logo": tool.logo.url if tool.logo else None,
                "average_rating": round(avg_rating or 0, 1),
                "total_reviews": reviews.count(),
                "good_count": good_count,
                "bad_count": bad_count
            },
            "reviews": ResumeToolReviewSerializer(reviews, many=True).data
        })
    



class CreateResumeToolReviewView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ResumeToolReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({"message": "Review added successfully"})

        return Response(serializer.errors, status=400)
    



class UpdateResumeToolReviewView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:
            review = ResumeToolReview.objects.get(id=pk)
        except ResumeToolReview.DoesNotExist:
            return Response({"error": "Review not found"}, status=404)

        
        if review.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        serializer = ResumeToolReviewSerializer(review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Review updated successfully"})

        return Response(serializer.errors, status=400)






class DeleteResumeToolReviewView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        review = ResumeToolReview.objects.get(id=pk)

        if review.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        review.delete()

        return Response({"message": "Review deleted"})
    



class ResumeToolReactionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ResumeToolReactionSerializer(data=request.data)

        if serializer.is_valid():

            tool = serializer.validated_data["tool"]
            reaction_type = serializer.validated_data["reaction"]

            try:
                reaction = ResumeToolReaction.objects.get(
                    user=request.user,
                    tool=tool
                )

                if reaction.reaction == reaction_type:
                    reaction.delete()
                    return Response({"message": "Reaction removed"})

                reaction.reaction = reaction_type
                reaction.save()

                return Response({"message": "Reaction updated"})

            except ResumeToolReaction.DoesNotExist:

                ResumeToolReaction.objects.create(
                    user=request.user,
                    tool=tool,
                    reaction=reaction_type
                )

                return Response({"message": "Reaction added"})

        return Response(serializer.errors, status=400)
    



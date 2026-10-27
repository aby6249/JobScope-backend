from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import JobPlatform, PlatformReview, PlatformReaction
from .serializers import JobPlatformSerializer, PlatformReviewSerializer, PlatformReactionSerializer
from dashboard.models import UserActivity



class PlatformListView(APIView):

    def get(self, request):

        platforms = JobPlatform.objects.annotate(
            avg_rating=Avg("reviews__rating")
        )

        data = []

        for platform in platforms:

            good_count = platform.reactions.filter(reaction="good").count()
            bad_count = platform.reactions.filter(reaction="bad").count()

            data.append({
                "id": platform.id,
                "name": platform.name,
                "website_url": platform.website_url,
                "description": platform.description,
                "logo": platform.logo.url if platform.logo else None,
                "average_rating": round(platform.avg_rating or 0, 1),
                "total_reviews": platform.reviews.count(),
                "good_count": good_count,
                "bad_count": bad_count
            })

        return Response(data)


class PlatformDetailView(APIView):

    def get(self, request, pk):

        platform = JobPlatform.objects.get(id=pk)

        UserActivity.objects.create(

            user=request.user,

            activity_type="platform",

            object_id=platform.id

        )

        avg_rating = platform.reviews.aggregate(
            avg=Avg("rating")
        )["avg"]

        reviews = PlatformReview.objects.filter(platform=platform)

        good_count = platform.reactions.filter(reaction="good").count()
        bad_count = platform.reactions.filter(reaction="bad").count()

        return Response({
            "platform": {
                "id": platform.id,
                "name": platform.name,
                "website_url": platform.website_url,
                "description": platform.description,
                "logo": platform.logo.url if platform.logo else None,
                "average_rating": round(avg_rating or 0, 1),
                "total_reviews": reviews.count(),
                "good_count": good_count,
                "bad_count": bad_count
            },
            "reviews": PlatformReviewSerializer(reviews, many=True).data
        })


class CreateReviewView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PlatformReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({
                "message": "Review added successfully"
            })

        return Response(serializer.errors, status=400)




class UpdateReviewView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:
            review = PlatformReview.objects.get(id=pk)
        except PlatformReview.DoesNotExist:
            return Response({"error": "Review not found"}, status=404)

    
        if review.user != request.user:
            return Response({"error": "Not allowed"}, status=403)

        serializer = PlatformReviewSerializer(review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Review updated successfully"})

        return Response(serializer.errors, status=400)






class DeleteReviewView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        review = PlatformReview.objects.get(id=pk)

        if review.user != request.user:
            return Response(
                {"error": "Not allowed"},
                status=403
            )

        review.delete()

        return Response({
            "message": "Review deleted"
        })


class PlatformReactionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PlatformReactionSerializer(data=request.data)

        if serializer.is_valid():

            platform = serializer.validated_data["platform"]
            reaction_type = serializer.validated_data["reaction"]

            try:
                reaction = PlatformReaction.objects.get(
                    user=request.user,
                    platform=platform
                )

        
                if reaction.reaction == reaction_type:
                    reaction.delete()
                    return Response({"message": "Reaction removed"})

            
                reaction.reaction = reaction_type
                reaction.save()

                return Response({"message": "Reaction updated"})

            except PlatformReaction.DoesNotExist:

                PlatformReaction.objects.create(
                    user=request.user,
                    platform=platform,
                    reaction=reaction_type
                )

                return Response({"message": "Reaction added"})

        return Response(serializer.errors, status=400)
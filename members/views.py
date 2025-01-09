from .serializers import MemberSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import date, timedelta
from .models import Members, Brand


class getMemberData(APIView):
    def get(self, request):
        try:
            member = Members.objects.all()
            serializer = MemberSerializer(member, many=True)
            return Response({
                "member": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CalculateOwnership(APIView):
    def get(self, request, *args, **kwargs):
        defaultBrand = Brand.objects.filter(name="default").first()
        totalTokens = defaultBrand.total_tokens
        tokenPrices = defaultBrand.token_prices
        month = 0
        expiryDate = defaultBrand.token_count_date + timedelta(days=defaultBrand.token_duration) * 30
        today = date.today()
        if today > expiryDate:
            return Response({"error": "Token count date has expired"}, status=status.HTTP_400_BAD_REQUEST)
        timePassed = today - defaultBrand.token_count_date
        if timePassed.days <= 30:
            month = .5
        elif timePassed.days <= 60:
            month = .3
        else:
            month = .2
        
        members = Members.objects.all()
        for member in members:
            role = member.role
            if role == 'super_founder':
                superFounderCount = len(members.filter(role='super_founder'))
                member.ownership = round((totalTokens * tokenPrices * .20 * month) / superFounderCount, 3)
                member.save()
            elif role == 'super_builder':
                superBuilderCount = len(members.filter(role='super_builder'))
                member.ownership = round((totalTokens * tokenPrices * .35 * month) / superBuilderCount, 3)
                member.save()
            elif role == 'super_communicator':
                superCommunicatorCount = len(members.filter(role='super_communicator'))
                member.ownership = round((totalTokens * tokenPrices * .25 * month) / superCommunicatorCount, 3)
                member.save()
            elif role == 'founder':
                founderCount = len(members.filter(role='founder'))
                member.ownership = round((totalTokens * tokenPrices * .05 * month) / founderCount, 3)
                member.save()
            elif role == 'builder':
                builderCount = len(members.filter(role='builder'))
                member.ownership = round((totalTokens * tokenPrices * .05 * month) / builderCount, 3)
                member.save()
            elif role == 'communicator':
                communicatorCount = len(members.filter(role='communicator'))
                member.ownership = round((totalTokens * tokenPrices * .05 * month) / communicatorCount, 3)
                member.save()
            elif role == 'tourist':
                touristCount = len(members.filter(role='tourist'))
                member.ownership = round((totalTokens * tokenPrices * .035 * month) / touristCount, 3)
                member.save()
            elif role == 'listener':
                listenerCount = len(members.filter(role='listener'))
                member.ownership = round((totalTokens * tokenPrices * .015 * month) / listenerCount, 3)
                member.save()
        return Response({"ownership has been set successfully"}, status=status.HTTP_200_OK)
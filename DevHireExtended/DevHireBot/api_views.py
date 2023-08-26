from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User  # Replace with your User model
from rest_framework.decorators import api_view
from rest_framework import status
import os


# @api_view(['GET', 'POST'])
@api_view(['GET'])
def initiate_resume_parsing(request):
    # request.session['resume_json_filePath'] = "C:\\Users\\maazi\\OneDrive\\Documents\\WORK\\CODE\\Prometheus\\empty\\DevHire-Extended\\DevHireExtended\\dumps\\2_data.json"  # Store the filename in the session
    # return JsonResponse({"result": True})
    if not request.user.resume:
        return Response({"message", "No resume was found."},status=status.HTTP_204_NO_CONTENT)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_relative_path = "resumes\\AshadAbdullah_resume_DsxBN9s.pdf"
    pdf_full_path = os.path.join(script_dir, pdf_relative_path)
    if os.path.exists(pdf_full_path):
        print(f"The file at {pdf_full_path} exists.")
    else:
        print(f"The file at {pdf_full_path} does not exist.")
    
    # filePath = main.make_json_from_resume(pdf_full_path, request.user.id)
    # request.session['resume_json_filePath'] = filePath  # Store the filename in the session
    return Response({"message", "Resume was found."}, status=status.HTTP_200_OK)

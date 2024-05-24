from django.shortcuts import render
from jobs.models import Job
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from jobs.serializers import JobPostSerializer
from jobs.models import Job
from jobs.serializers import JobGetSerializer
from django.db.models import Q
from search_slugs.models import SearchSlugs
from search_slugs.serializers import SearchSlugSerializers
from job_categoery.models import JobCategory
from job_categoery.serializer import AvailableJobCategoerySerializer
from intern_job_application.models import JobApplication
from available_skills.serializer import AvailableSkillSerializer
from available_skills.models import AvailableSkill
from sub_categoery.models import SubCategory
from sub_categoery.serializer import SubCategoerySerializer

class JobPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            if id is not None:    
                if (request.user.user_type == "company"):
                    job_data = Job.objects.filter(Q(company = id) & Q(company_user = request.user.id))
                    job_serializer = JobGetSerializer(job_data, many=True)
                    return Response(job_serializer.data, status=status.HTTP_200_OK)

            else:
                if(request.user.user_type == "user"):
                    applied_job_ids = JobApplication.objects.filter(user =request.user.id).values_list('job', flat=True)
                    print("----34-----")
                    print(applied_job_ids)
                    job_data = Job.objects.filter(~Q(id__in=applied_job_ids))
                    job_serializer = JobGetSerializer(job_data, many=True)
                    
                    # Search Title Slug 
                    search_title_data = SearchSlugs.objects.filter(~Q(job_title_slug__isnull=True))
                    search_title_slug_serailzer = SearchSlugSerializers(search_title_data , many=True)

                    # Search Location Slug
                    search_location_data = SearchSlugs.objects.filter(~Q(location_slug__isnull=True))
                    search_location_serializer = SearchSlugSerializers(search_location_data , many=True)

                    # Categoery Slug
                    job_categoery = JobCategory.objects.all()
                    job_categoery_serializer = AvailableJobCategoerySerializer(job_categoery, many=True)

                    # Sub Categoery
                    subcategoery_data = SubCategory.objects.filter()
                    subcategoery_serializer = SubCategoerySerializer(subcategoery_data, many=True)

                    return Response({"all_jobs":job_serializer.data,
                                "search_title_keywords": search_title_slug_serailzer.data,
                                "search_location_slug": search_location_serializer.data,
                                "search_categoery" : job_categoery_serializer.data  ,
                                "sub_categoery" : subcategoery_serializer.data}, status=status.HTTP_200_OK)
                elif(request.user.user_type == "company"):

                    available_skill = AvailableSkill.objects.all()
                    available_skill_serializer = AvailableSkillSerializer(available_skill, many=True)

                    # Available Job Categoeries
                    available_categoery = JobCategory.objects.filter(is_active = True)
                    available_categoery_serailzer = AvailableJobCategoerySerializer(available_categoery, many=True)

                    # Sub Categoery
                    subcategoery_data = SubCategory.objects.filter()
                    subcategoery_serializer = SubCategoerySerializer(subcategoery_data, many=True)

                    return Response({"aviable_skills": available_skill_serializer.data,
                                   "categoery_option": available_categoery_serailzer.data,
                                   "sub_categoery" : subcategoery_serializer.data
                                   })

        except Exception as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id = None):
        try:
            if (request.user.user_type == "company"):
                job_serializer = JobPostSerializer(data=request.data)
                if job_serializer.is_valid():
                    try:
                        slug_data = {
                            "job_title_slug": request.data.get("job_title"),
                            "location_slug": request.data.get("location")
                        }
                        # Try saving with job_title_slug
                        slug_serializer = SearchSlugSerializers(data=slug_data)
                        if slug_serializer.is_valid():
                            slug_serializer.save()
                        else:
                            job_title_errors = slug_serializer.errors.get('job_title_slug', [])
                            location_errors = slug_serializer.errors.get('location_slug', [])
                            # Check if the uniqueness error occurred for job_title_slug
                            if any(error.code == 'unique' for error in job_title_errors):
                                # Retry saving with location_slug
                                slug_data['job_title_slug'] = None
                                slug_serializer = SearchSlugSerializers(data=slug_data)
                                if slug_serializer.is_valid():
                                    slug_serializer.save()
                                else:
                                    print(slug_serializer.errors)
                            elif any(error.code == 'unique' for error in location_errors):
                                # Retry saving with job_title_slug
                                slug_data['location_slug'] = None
                                slug_serializer = SearchSlugSerializers(data=slug_data)
                                if slug_serializer.is_valid():
                                    slug_serializer.save()
                                else:
                                    print(slug_serializer.errors)
                    except Exception as e:
                        print(e)
                        pass
                    job_serializer.save()
                    return Response({"message": "Job Posted Successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
            else:
                return Response({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id=None):
        if id is not None:
            pass
        else:
            return Response({"error": "method not allowed"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id = None):
        if id is None or request.user.user_type != "company":
            return Response({"error" : "Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if (request.user.user_type == "company"):
                jobs = Job.objects.filter(company_user = request.user.id)
                try:
                    selected_job = jobs.get(id = id)
                    selected_job.delete()
                    return Response({"message" : "Deleted Successfully"}, status=status.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    return Response({"error" : "No Jobs Found"}, status=status.HTTP_400_BAD_REQUEST)



class JobSearchView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            # Define the available query parameters
            query_params = ['location', 'job_title', 'job_categoery', 'sub_categoery']
            # Create a dictionary to store the filters
            filters = {}
            # Iterate through the query parameters and add filters if they exist
            for param in query_params:
                param_value = request.query_params.get(param)
                if param_value is not None:
                    filters[param] = param_value

            applied_job_ids = JobApplication.objects.filter(user = request.user.id).values_list('job', flat=True)
            job_not_applied = Job.objects.filter(~Q(id__in=applied_job_ids))
            job_data = job_not_applied.filter(**filters) if filters else job_not_applied
            job_serializer = JobGetSerializer(job_data, many=True)
            
            return Response(job_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobAuthSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            # Define the available query parameters
            query_params = ['location', 'job_title', 'job_categoery', 'sub_categoery']
            # Create a dictionary to store the filters  
            filters = {}
            # Iterate through the query parameters and add filters if they exist
            for param in query_params:
                param_value = request.query_params.get(param)
                if param_value is not None:
                    filters[param] = param_value
            applied_job_ids = JobApplication.objects.filter(user = request.user.id).values_list('job', flat=True)
            job_not_applied = Job.objects.filter(~Q(id__in=applied_job_ids))
            print(filters)
            job_data = job_not_applied.filter(**filters) if filters else job_not_applied
            job_serializer = JobGetSerializer(job_data, many=True)
            
            return Response(job_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


        
class JobsUnAuthGetView(APIView):
    def get(self, request, id = None):     
        # Job 
        applied_job_ids = JobApplication.objects.filter(user =request.user.id).values_list('job', flat=True)
        job_data = Job.objects.filter(~Q(id__in=applied_job_ids))
        job_serializer = JobGetSerializer(job_data, many=True)
        
        # Search Title Slug 
        search_title_data = SearchSlugs.objects.filter(~Q(job_title_slug__isnull=True))
        search_title_slug_serailzer = SearchSlugSerializers(search_title_data , many=True)

        # Search Location Slug
        search_location_data = SearchSlugs.objects.filter(~Q(location_slug__isnull=True))
        search_location_serializer = SearchSlugSerializers(search_location_data , many=True)

        # Categoery Slug
        job_categoery = JobCategory.objects.all()
        job_categoery_serializer = AvailableJobCategoerySerializer(job_categoery, many=True)

        # Sub Categoery
        subcategoery_data = SubCategory.objects.filter()
        subcategoery_serializer = SubCategoerySerializer(subcategoery_data, many=True)

        return Response({"all_jobs":job_serializer.data,
                    "search_title_keywords": search_title_slug_serailzer.data,
                    "search_location_slug": search_location_serializer.data,
                    "search_categoery" : job_categoery_serializer.data  ,
                    "sub_categoery" : subcategoery_serializer.data}, status=status.HTTP_200_OK)
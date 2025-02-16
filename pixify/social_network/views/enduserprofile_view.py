from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.views import View
from ..services import user_service
from ..constants import Gender
from ..constants import RelationShipStatus


class EnduserprofileView(View):
    def get(self, request):
        return render(request, 'enduser/profile/index.html')
class UserprofileView(View):
    def get(self, request):
        return render(request, 'enduser/profile/userprofile.html')

# Work By Badhan
class EnduserprofileUpdateView(View):
    def get(self, request, user_id):
        user_details = user_service.get_user_details(user_id)
        print(user_details)
        return render(request, 'enduser/profile/editprofile.html', {'user_details': user_details})

    def post(self, request, user_id):
        user_details = user_service.get_user_details(user_id)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        country = request.POST.get('country')
        bio= request.POST.get('bio')
        if request.method == 'POST':
         hobbies = request.POST.get('hobbies', '')
         hobbies_list = [hobby.strip() for hobby in hobbies.split(',')] if hobbies else []
         hobbies = hobbies_list
        # Convert gender value to integer
        gender_mapping = {'Male': Gender.MALE.value, 'Female': Gender.FEMALE.value, 'Other': Gender.OTHER.value}
        gender = gender_mapping.get(gender, None)
        # convert relationship into integer
        relationship_status = request.POST.get('relationship_status')
        relationship_status_mapping = {
            'Single': RelationShipStatus.SINGLE.value,
            'Married': RelationShipStatus.MARRIED.value,
            'Divorced': RelationShipStatus.DIVORCED.value,
            'Widowed': RelationShipStatus.WIDOWED.value,
            'Other': RelationShipStatus.OTHER.value,
        }
        relationship_status = relationship_status_mapping.get(relationship_status, None)
        profile_picture = request.FILES.get('profile_picture')


        user_service.update_user(user_id, first_name, last_name, email, phone, gender,address,dob,country,bio,hobbies,relationship_status, profile_picture)

        return render(request, 'enduser/profile/index.html', {'user_details': user_details, 'errors': "An error occurred"})


# End by Badhan


def edit_information(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserProfileForm()
    return render(request, 'edit_information.html', {'form': form})

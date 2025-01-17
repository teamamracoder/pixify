import base64
from django.core.files.base import ContentFile
from ..models import User
from PIL import Image
import face_recognition  # Assumes you're using the `face_recognition` library

def save_user_image(image_data, user_id):
    try:
        # Decode base64 image
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]  # Extract file extension
        image_file = ContentFile(base64.b64decode(imgstr), name=f"captured_image.{ext}")

        # Fetch the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {'success': False, 'message': 'User not found.'}

        # If user doesn't have a verification image, save the new image
        if not user.verification_image:
            user.verification_image = image_file
            user.is_verified = True
            user.save()
            return {
                'success': True, 
                'message': 'Verified successfully.',  # Return image URL
            }

        else:
            # Compare new image with the existing image
            try:
                existing_image_path = user.verification_image.path
                existing_image = face_recognition.load_image_file(existing_image_path)

                # Load the new image
                new_image = face_recognition.load_image_file(image_file)

                # Encode the faces in both images
                existing_face_encodings = face_recognition.face_encodings(existing_image)
                new_face_encodings = face_recognition.face_encodings(new_image)

                # If either image has no faces detected, return an error
                if not existing_face_encodings or not new_face_encodings:
                    return {'success': False, 'message': 'Could not detect faces in one or both images.'}

                # Compare faces
                match = face_recognition.compare_faces([existing_face_encodings[0]], new_face_encodings[0])

                if match[0]:
                    user.is_verified = True
                    user.save()
                    return {
                        'success': True, 
                        'message': 'Already Verified!', 
                        'is_verified': user.is_verified,
                        'image_url': user.verification_image.url  # Return image URL
                    }
                else:
                    return {'success': False, 'message': 'Face does not match the existing image.', 'is_verified': user.is_verified}

            except Exception as e:
                return {'success': False, 'message': f"An error occurred during face comparison: {str(e)}"}

    except Exception as e:
        return {'success': False, 'message': f"An unexpected error occurred: {str(e)}"}



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

        # Load the new image
        new_image = face_recognition.load_image_file(image_file)
        new_face_encodings = face_recognition.face_encodings(new_image)

        # Check if a face is detected in the new image
        if not new_face_encodings:
            return {'success': False, 'message': 'No face detected in the uploaded image.'}

        # Handle cases where the user doesn't have a verification image
        if not user.verification_image:
            # Retrieve all users with verification images (excluding the current user)
            users_with_images = User.objects.exclude(verification_image__isnull=True).exclude(id=user.id)

            # Load and encode all verification images
            all_face_encodings = []
            for other_user in users_with_images:
                try:
                    existing_image_path = other_user.verification_image.path
                    existing_image = face_recognition.load_image_file(existing_image_path)
                    encodings = face_recognition.face_encodings(existing_image)
                    if encodings:
                        all_face_encodings.append(encodings[0])  # Append the first encoding
                except Exception as e:
                    print(f"Error processing image for user {other_user.id}: {e}")  # Log the error for debugging

            # Check if the new face matches any existing faces in the database
            match = any(face_recognition.compare_faces(all_face_encodings, new_face_encodings[0]))
            if match:
                return {'success': False, 'message': 'Face already exists in the database.'}

            # If no match, save the new verification image for the user
            user.verification_image = image_file
            user.is_verified = False
            user.save()
            return {
                'success': True,
                'message': 'Image saved for future verification.',
                'is_verified': user.is_verified,
                'image_url': user.verification_image.url,
            }

        # If the user already has a verification image
        else:
            try:
                existing_image_path = user.verification_image.path
                existing_image = face_recognition.load_image_file(existing_image_path)
                existing_face_encodings = face_recognition.face_encodings(existing_image)

                # If no faces are detected in the existing verification image, return an error
                if not existing_face_encodings:
                    return {'success': False, 'message': 'No face detected in the existing verification image.'}

                # Compare the new face encoding with the existing verification image
                match = face_recognition.compare_faces([existing_face_encodings[0]], new_face_encodings[0])

                if match[0]:
                    user.is_verified = True
                    user.save()
                    return {
                        'success': True,
                        'message': 'User verified successfully!',
                        'is_verified': user.is_verified,
                        'image_url': user.verification_image.url,
                    }
                else:
                    return {'success': False, 'message': 'Face does not match the existing image.', 'is_verified': user.is_verified}

            except Exception as e:
                return {'success': False, 'message': f"An error occurred during face comparison: {str(e)}"}

    except Exception as e:
        return {'success': False, 'message': f"An unexpected error occurred: {str(e)}"}
    
def user(user_id):
    user_details=User.objects.filter(id=user_id).values('verification_image').first()
    return user_details    

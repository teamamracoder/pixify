from django.views import View
import json
from django.http import JsonResponse
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error
from ..services import message_reaction_service

class MessageReactionsListView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, message_id):
        try:
            reactions =message_reaction_service.get_active_message_reactions(message_id)
            reaction_data = [
                {
                    'reaction': reaction.reaction_id.value,
                    'reaction_count': message_reaction_service.get_reaction_count(message_id, reaction.reaction_id)
                }
                for reaction in reactions
            ]
            return JsonResponse({'reactions': reaction_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class MessageReactionCreateView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request):
        try:
            data = json.loads(request.body)
            message_id = data.get('message_id')
            reaction_id = data.get('reaction_id')
            user = request.user
            reaction = message_reaction_service.get_reaction_by_name(reaction_id)
            if not reaction:
                return JsonResponse({'success': False, 'error': 'Invalid reaction'}, status=400)
            message_reaction_service.create_or_update_message_reaction(message_id, user, reaction)
            new_count = message_reaction_service.get_reaction_count(message_id, reaction)
            return JsonResponse({'success': True, 'new_count': new_count}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

class MessageReactionDeleteView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request):
        try:
            data = json.loads(request.body)
            message_id = data.get('message_id')
            user = request.user
            reaction_instance = message_reaction_service.get_active_reaction(message_id, user)

            if not reaction_instance:
                return JsonResponse({'success': False, 'error': 'Reaction not found'}, status=400)
            message_reaction_service.deactivate_reaction(reaction_instance)

            return JsonResponse({'success': True, 'message': 'Reaction deleted successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

class ReactionDetailsView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, message_id, reaction_type):
        try:
            reaction_data = message_reaction_service.get_reaction_details(message_id, reaction_type)
            return JsonResponse(reaction_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    


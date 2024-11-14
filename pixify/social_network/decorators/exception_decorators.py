from functools import wraps
import traceback
from django.http import JsonResponse
from social_network.utils.common_utils import print_log


def catch_error(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except Exception as e:
            stack_trace = traceback.format_exc()
            print_log(stack_trace)
            return JsonResponse(
                {
                    "status": "error",
                    "status_code": 500,
                    "message": str(e),
                    "stack_trace": stack_trace.replace("\n", "   💥💥💥   "),
                },
                status=500,
            )

    return _wrapped_view

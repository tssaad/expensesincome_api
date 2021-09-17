from django.http import JsonResponse, response


def error_404(request, exception):
    context = {
        'message': 'The endpoint is not found',
        'status_code' : 404
    }

    response = JsonResponse(data=context)
    response.status_code = 404

    return response

def error_500(request):
    context = {
        'message': 'An error occuried! it is us!! Sorry!!',
        'status_code' : 500
    }

    response = JsonResponse(data=context)
    response.status_code = 500

    return response

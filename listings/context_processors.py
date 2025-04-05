def user_info(request):
    """
    Context processor to make user information available in all templates.
    """
    context = {
        'user_id': request.session.get('user_id', None),
        'user_type': request.session.get('user_type', None),
        'user_name': request.session.get('user_name', None),
        'user_email': request.session.get('user_email', None),
        'is_authenticated': 'user_id' in request.session,
    }
    return context 
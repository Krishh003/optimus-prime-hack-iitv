from django import template

register = template.Library()

@register.filter
def filter_active_events(requests):
    """
    Filter out requests where the associated event has been deleted and remove duplicates.
    """
    seen_ids = set()
    unique_active_requests = []
    
    for request in requests:
        if request.get('event_exists', False) and request.get('id') not in seen_ids:
            seen_ids.add(request.get('id'))
            unique_active_requests.append(request)
    
    return unique_active_requests 
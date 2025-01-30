from django import template

register = template.Library()

@register.filter
def contains_event(user_events, event_id):
    return any(event.get('id') == event_id for event in user_events)

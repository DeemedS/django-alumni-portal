from django.shortcuts import get_object_or_404
from articles.models import BodyText, BodyImage, SubTitle
from events.models import Event

def get_ordered_content(content):
    model_map = {
        'bodytext': BodyText,
        'subtitle': SubTitle,
        'bodyimage': BodyImage,
        'event': Event,
    }
    
    ordered_content = [
        {'type': model_name, 'object': get_object_or_404(model_map[model_name], id=obj_id)}
        for model_name, obj_id in (item.split('-') for item in content.order)
    ]
    
    return ordered_content
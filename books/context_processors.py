from .models import Genre

def genres_context(request):
    return {
        'genres': Genre.objects.all().order_by('id')
    }
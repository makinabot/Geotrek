from django.conf import settings as settings_ # import the settings file

from caminae import __version__


def settings(request):
    return dict(
        TITLE=settings_.TITLE,
        DEBUG=settings_.DEBUG,
        VERSION=__version__,
        DATE_INPUT_FORMAT_JS=settings_.DATE_INPUT_FORMATS[0].replace('%Y', 'yyyy').replace('%m', 'mm').replace('%d', 'dd'),
        
        LAYERCOLOR_PATHS=settings_.LAYERCOLOR_PATHS,
        LAYERCOLOR_LAND=settings_.LAYERCOLOR_LAND,
        LAYERCOLOR_OTHERS=settings_.LAYERCOLOR_OTHERS,
    )
#общая переменная для всех шаблонов {{ year }}

import datetime
def year(request):
    """Добавляет в контекст переменную greeting с приветствием."""
    return {
        'year': str(datetime.datetime.now().year),
        }
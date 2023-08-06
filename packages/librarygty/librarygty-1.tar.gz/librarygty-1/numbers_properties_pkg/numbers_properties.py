from datetime import datetime
from django.utils import timezone


class numberProperties:
    # datetime(year, month, day, hour, minute, second)
    def days_remaining(self,obj):
        if obj.returned:
            return 'returned'
        elif obj.return_date :
            y,m,d=str(timezone.now().date()).split('-')
            today=datetime.date(int(y),int(m),int(d))
            y2,m2,d2=str(obj.return_date.date()).split('-')
            lastdate=datetime.date(int(y2),int(m2),int(d2))
            if lastdate>today:
                return '{} days'.format((lastdate-today).days)
            return '{} days passed'.format((today-lastdate).days)
        return 'not issued'

   
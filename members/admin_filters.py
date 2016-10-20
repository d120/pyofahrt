from django.contrib import admin

class MemberQueueFilter(admin.SimpleListFilter):
    title = "Anmeldeliste"
    parameter_name = "queuelist"

    def lookups(self, request, modeladmin):
        return (
            ('queue', 'Warteschlange'),
            ('cond', 'temporär angemeldet'),
            ('fin', 'festangemeldet')
        )

    def queryset(self, request, queryset):
        if self.value() == "fin":
            return queryset.filter(money_received=True)
        elif self.value() == "cond":
            return queryset.filter(money_received=False).filter(queue=True)
        elif self.value() == "queue":
            return queryset.filter(money_received=False).filter(queue=False)
        else:
            print(self.value())
            return queryset.none()

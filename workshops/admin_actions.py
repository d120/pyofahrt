def set_accepted(modeladmin, request, queryset):
    queryset.update(accepted=True, proved=True)
    modeladmin.message_user(
        request, "{} Workshops wurden auf bestätigt gesetzt.".format(queryset.count())
    )


set_accepted.short_description = "Workshops auf bestätigt und geprüft setzen"

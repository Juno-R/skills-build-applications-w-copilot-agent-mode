from django.contrib import admin
from django.db.models import Count

from .models import Activity, LeaderboardEntry, Team, User, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'member_count')
    search_fields = ('name', 'description')
    list_filter = ('name',)

    def member_count(self, obj):
        return obj.user_set.count()
    member_count.short_description = 'Members'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'team', 'activity_count')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('team',)
    list_editable = ('team',)

    def activity_count(self, obj):
        return obj.activity_set.count()
    activity_count.short_description = 'Activities'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_type', 'duration_minutes', 'distance_km', 'timestamp')
    list_filter = ('activity_type', 'timestamp', 'user__team')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    date_hierarchy = 'timestamp'
    list_editable = ('duration_minutes', 'distance_km')


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'rank', 'updated_at')
    list_filter = ('rank', 'updated_at', 'user__team')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    date_hierarchy = 'updated_at'
    list_editable = ('score', 'rank')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'scheduled_at', 'description_short')
    list_filter = ('scheduled_at', 'user__team')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'name')
    date_hierarchy = 'scheduled_at'
    list_editable = ('scheduled_at',)

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

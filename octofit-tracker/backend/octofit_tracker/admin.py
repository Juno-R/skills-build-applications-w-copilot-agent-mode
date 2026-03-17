from django.contrib import admin

from .models import Activity, LeaderboardEntry, Team, User, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'team')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('team',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_type', 'duration_minutes', 'distance_km', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__email',)


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'rank', 'updated_at')
    list_filter = ('rank',)
    search_fields = ('user__email',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'scheduled_at')
    list_filter = ('scheduled_at',)
    search_fields = ('user__email', 'name')

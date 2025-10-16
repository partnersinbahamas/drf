from rest_framework.throttling import UserRateThrottle

class RoleBasedRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if not request.user:
            self.scope = "anon"

        if request.user and request.user.is_staff:
            self.scope = "admin"

        if request.user and request.user.is_authenticated:
            self.scope = "user"

        return super().get_cache_key(request, view)

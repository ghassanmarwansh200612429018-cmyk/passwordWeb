"""
Auto-logout middleware: expires sessions after inactivity.
Works alongside SESSION_COOKIE_AGE in settings.py.
Also tracks last activity timestamp for more granular control.
"""

import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


class AutoLogoutMiddleware:
    """
    Checks the time of the user's last request.
    If more than SESSION_COOKIE_AGE seconds have passed, log out.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = time.time()

            if last_activity and (now - last_activity) > settings.SESSION_COOKIE_AGE:
                logout(request)
                messages.warning(request, 'Your session has expired due to inactivity. Please log in again.')
                return redirect('login')

            request.session['last_activity'] = now

        response = self.get_response(request)
        return response

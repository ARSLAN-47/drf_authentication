from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Convert token expiration times to milliseconds
    access_token_expiration_ms = int(refresh.access_token['exp']) * 1000
    refresh_token_expiration_ms = int(refresh['exp']) * 1000

    return {
        'refresh': refresh_token,
        'access': access_token,
        'access_expiry': access_token_expiration_ms,
        'refresh_expiry': refresh_token_expiration_ms,
    }
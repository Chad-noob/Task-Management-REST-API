from fastapi import Header, HTTPException, status

from .database import get_connection



def get_current_user(authorization: str = Header(default='')):
    """Read the Bearer token and resolve the logged-in user."""
    if not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header is missing or invalid',
        )

    token = authorization.split(' ', 1)[1].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token was not provided',
        )

    connection = get_connection()
    try:
        user = connection.execute(
            '''
            SELECT u.id, u.name, u.email, u.created_at
            FROM sessions s
            INNER JOIN users u ON u.id = s.user_id
            WHERE s.token = ?
            ''',
            (token,),
        ).fetchone()
    finally:
        connection.close()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Session token is invalid or has already expired',
        )

    return dict(user)

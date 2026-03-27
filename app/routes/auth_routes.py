from fastapi import APIRouter, HTTPException, status

from ..database import get_db_cursor
from ..schemas import LoginRequest, RegisterRequest
from ..security import generate_session_token, hash_password, verify_password

router = APIRouter(prefix='/api/auth', tags=['Authentication'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest):
    with get_db_cursor() as (_, cursor):
        existing_user = cursor.execute(
            'SELECT id FROM users WHERE email = ?',
            (payload.email,),
        ).fetchone()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='An account with this email already exists',
            )

        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (payload.name, payload.email, hash_password(payload.password)),
        )
        new_user_id = cursor.lastrowid

        session_token = generate_session_token()
        cursor.execute(
            'INSERT INTO sessions (user_id, token) VALUES (?, ?)',
            (new_user_id, session_token),
        )

        user_row = cursor.execute(
            'SELECT id, name, email, created_at FROM users WHERE id = ?',
            (new_user_id,),
        ).fetchone()

    return {
        'success': True,
        'message': 'Registration completed successfully',
        'data': {
            'user': dict(user_row),
            'token': session_token,
        },
    }


@router.post('/login')
def login_user(payload: LoginRequest):
    with get_db_cursor() as (_, cursor):
        user_row = cursor.execute(
            'SELECT * FROM users WHERE email = ?',
            (payload.email,),
        ).fetchone()

        if user_row is None or not verify_password(payload.password, user_row['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password',
            )

        session_token = generate_session_token()
        cursor.execute(
            'INSERT INTO sessions (user_id, token) VALUES (?, ?)',
            (user_row['id'], session_token),
        )

    return {
        'success': True,
        'message': 'Login successful',
        'data': {
            'user': {
                'id': user_row['id'],
                'name': user_row['name'],
                'email': user_row['email'],
                'created_at': user_row['created_at'],
            },
            'token': session_token,
        },
    }

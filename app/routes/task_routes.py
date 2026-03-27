from math import ceil
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..database import get_connection, get_db_cursor
from ..dependencies import get_current_user
from ..schemas import TaskCreateRequest, TaskStatusUpdateRequest

router = APIRouter(prefix='/api/tasks', tags=['Tasks'])
VALID_STATUSES = {'pending', 'in_progress', 'completed'}


@router.post('', status_code=status.HTTP_201_CREATED)
def create_new_task(payload: TaskCreateRequest, current_user=Depends(get_current_user)):
    with get_db_cursor() as (_, cursor):
        cursor.execute(
            '''
            INSERT INTO tasks (user_id, title, description, status)
            VALUES (?, ?, ?, ?)
            ''',
            (
                current_user['id'],
                payload.title,
                payload.description,
                payload.status,
            ),
        )
        new_task_id = cursor.lastrowid

        task_row = cursor.execute(
            '''
            SELECT id, title, description, status, created_at
            FROM tasks
            WHERE id = ? AND user_id = ?
            ''',
            (new_task_id, current_user['id']),
        ).fetchone()

    return {
        'success': True,
        'message': 'Task created successfully',
        'data': dict(task_row),
    }


@router.get('')
def list_tasks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    status_filter: Optional[str] = Query(default=None, alias='status'),
    current_user=Depends(get_current_user),
):
    if status_filter and status_filter not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Status filter must be pending, in_progress, or completed',
        )

    query_params = [current_user['id']]
    where_clause = 'WHERE user_id = ?'

    if status_filter:
        where_clause += ' AND status = ?'
        query_params.append(status_filter)

    offset = (page - 1) * limit
    connection = get_connection()
    try:
        total_count = connection.execute(
            f'SELECT COUNT(*) AS total FROM tasks {where_clause}',
            query_params,
        ).fetchone()['total']

        task_rows = connection.execute(
            f'''
            SELECT id, title, description, status, created_at
            FROM tasks
            {where_clause}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            ''',
            (*query_params, limit, offset),
        ).fetchall()
    finally:
        connection.close()

    return {
        'success': True,
        'message': 'Tasks fetched successfully',
        'data': [dict(row) for row in task_rows],
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total_count,
            'total_pages': ceil(total_count / limit) if total_count else 0,
        },
    }


@router.patch('/{task_id}/status')
def change_task_status(
    task_id: int,
    payload: TaskStatusUpdateRequest,
    current_user=Depends(get_current_user),
):
    with get_db_cursor() as (_, cursor):
        existing_task = cursor.execute(
            'SELECT id FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, current_user['id']),
        ).fetchone()

        if existing_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found for the current user',
            )

        cursor.execute(
            'UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?',
            (payload.status, task_id, current_user['id']),
        )

        updated_task = cursor.execute(
            '''
            SELECT id, title, description, status, created_at
            FROM tasks
            WHERE id = ? AND user_id = ?
            ''',
            (task_id, current_user['id']),
        ).fetchone()

    return {
        'success': True,
        'message': 'Task status updated',
        'data': dict(updated_task),
    }


@router.delete('/{task_id}')
def remove_task(task_id: int, current_user=Depends(get_current_user)):
    with get_db_cursor() as (_, cursor):
        existing_task = cursor.execute(
            'SELECT id FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, current_user['id']),
        ).fetchone()

        if existing_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found for the current user',
            )

        cursor.execute(
            'DELETE FROM tasks WHERE id = ? AND user_id = ?',
            (task_id, current_user['id']),
        )

    return {
        'success': True,
        'message': f'Task {task_id} deleted successfully',
    }

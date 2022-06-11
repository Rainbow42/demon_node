from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Request, Response

router = APIRouter()


@router.get(path='/test/',
            name='Test',
            description='Test',
            operation_id='api_Test',
            tags=['Test'],
            status_code=200)
async def tests(request: Request = None):
    return "test"

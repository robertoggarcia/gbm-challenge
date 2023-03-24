from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/_healthcheck")
def healthcheck():
    """
    Health check end-point
    """
    return Response(content="OK")

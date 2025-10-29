from fastapi import HTTPException, status


async def deprecated_endpoint():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is deprecated and not yet implemented. Please check back later.",
    )

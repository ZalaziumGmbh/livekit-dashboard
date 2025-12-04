"""Agent management routes"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from urllib.parse import quote

from app.services.livekit import LiveKitClient, get_livekit_client
from app.security.basic_auth import requires_admin, get_current_user
from app.security.csrf import get_csrf_token, verify_csrf_token


router = APIRouter()


@router.get("/agents", response_class=HTMLResponse, dependencies=[Depends(requires_admin)])
async def agents_index(
    request: Request,
    flash_message: Optional[str] = None,
    flash_type: Optional[str] = None,
    lk: LiveKitClient = Depends(get_livekit_client),
):
    """List all deployed agents and their status"""
    agent_analytics = await lk.get_agent_analytics()
    rooms, _ = await lk.list_rooms()
    current_user = get_current_user(request)

    return request.app.state.templates.TemplateResponse(
        "agents/index.html.j2",
        {
            "request": request,
            "analytics": agent_analytics,
            "agents": agent_analytics.get('agent_list', []),
            "active_agents": agent_analytics.get('active_agents', []),
            "configured_agents": agent_analytics.get('configured_agents', []),
            "rooms": rooms,
            "current_user": current_user,
            "sip_enabled": lk.sip_enabled,
            "csrf_token": get_csrf_token(request),
            "flash_message": flash_message,
            "flash_type": flash_type,
        },
    )


@router.post("/agents/dispatch", dependencies=[Depends(requires_admin)])
async def create_agent_dispatch(
    request: Request,
    csrf_token: str = Form(...),
    room_name: str = Form(...),
    agent_name: str = Form(...),
    metadata: Optional[str] = Form(None),
    lk: LiveKitClient = Depends(get_livekit_client),
):
    """Create a new agent dispatch to join a room"""
    await verify_csrf_token(request)

    try:
        await lk.create_agent_dispatch(
            room_name=room_name,
            agent_name=agent_name,
            metadata=metadata,
        )

        success_msg = quote(f"Successfully dispatched agent '{agent_name}' to room '{room_name}'")
        return RedirectResponse(
            url=f"/agents?flash_message={success_msg}&flash_type=success", status_code=303
        )
    except Exception as e:
        error_msg = str(e)
        print(f"Error creating agent dispatch: {e}")
        import traceback
        traceback.print_exc()

        encoded_error = quote(f"Failed to dispatch agent: {error_msg}")
        return RedirectResponse(
            url=f"/agents?flash_message={encoded_error}&flash_type=danger", status_code=303
        )


@router.post("/agents/dispatch/delete", dependencies=[Depends(requires_admin)])
async def delete_agent_dispatch(
    request: Request,
    csrf_token: str = Form(...),
    dispatch_id: str = Form(...),
    room_name: str = Form(...),
    lk: LiveKitClient = Depends(get_livekit_client),
):
    """Delete an agent dispatch"""
    await verify_csrf_token(request)

    try:
        await lk.delete_agent_dispatch(
            dispatch_id=dispatch_id,
            room_name=room_name,
        )

        success_msg = quote("Successfully removed agent dispatch")
        return RedirectResponse(
            url=f"/agents?flash_message={success_msg}&flash_type=success", status_code=303
        )
    except Exception as e:
        error_msg = str(e)
        print(f"Error deleting agent dispatch: {e}")
        import traceback
        traceback.print_exc()

        encoded_error = quote(f"Failed to remove agent dispatch: {error_msg}")
        return RedirectResponse(
            url=f"/agents?flash_message={encoded_error}&flash_type=danger", status_code=303
        )

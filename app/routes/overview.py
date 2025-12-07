"""Overview/Dashboard routes - Simplified for SIP telephony"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.services.livekit import LiveKitClient, get_livekit_client
from app.security.basic_auth import requires_admin, get_current_user
from app.security.csrf import get_csrf_token


router = APIRouter()


@router.get("/", response_class=HTMLResponse, dependencies=[Depends(requires_admin)])
async def overview(
    request: Request,
    lk: LiveKitClient = Depends(get_livekit_client),
):
    """Display overview dashboard focused on SIP telephony"""
    # Get server info
    server_info = await lk.get_server_info()

    # Get SIP analytics if enabled
    sip_analytics = None
    configured_agents = []
    active_rooms = 0
    total_participants = 0

    if lk.sip_enabled:
        try:
            sip_analytics = await lk.get_sip_analytics()
            configured_agents = await lk.get_configured_agents()

            # Get active rooms (call rooms)
            rooms, _ = await lk.list_rooms()
            active_rooms = len(rooms)
            total_participants = sum(getattr(r, 'num_participants', 0) for r in rooms)
        except Exception as e:
            print(f"Error getting SIP data: {e}")

    current_user = get_current_user(request)

    return request.app.state.templates.TemplateResponse(
        "index.html.j2",
        {
            "request": request,
            "server_info": server_info,
            "sip_analytics": sip_analytics,
            "configured_agents": configured_agents,
            "active_rooms": active_rooms,
            "total_participants": total_participants,
            "current_user": current_user,
            "sip_enabled": lk.sip_enabled,
            "csrf_token": get_csrf_token(request),
        },
    )

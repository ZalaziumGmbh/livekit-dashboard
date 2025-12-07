"""Agent management routes - Simplified for SIP telephony"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.services.livekit import LiveKitClient, get_livekit_client
from app.security.basic_auth import requires_admin, get_current_user
from app.security.csrf import get_csrf_token


router = APIRouter()


@router.get("/agents", response_class=HTMLResponse, dependencies=[Depends(requires_admin)])
async def agents_index(
    request: Request,
    lk: LiveKitClient = Depends(get_livekit_client),
):
    """List agents configured in SIP dispatch rules"""
    # Get configured agents from SIP dispatch rules
    configured_agents = await lk.get_configured_agents()

    # Get active agents in rooms
    active_agents = await lk.get_agents_in_rooms()
    active_names = set(a.get('identity', '').split('-')[0] for a in active_agents)

    # Build simple agent list
    agents = []
    for agent in configured_agents:
        agents.append({
            "name": agent.get("name", "Unknown"),
            "rule_name": agent.get("rule_name", "Unknown"),
            "is_active": agent.get("name", "") in active_names,
        })

    current_user = get_current_user(request)

    return request.app.state.templates.TemplateResponse(
        "agents/index.html.j2",
        {
            "request": request,
            "agents": agents,
            "active_count": len(active_agents),
            "current_user": current_user,
            "sip_enabled": lk.sip_enabled,
            "csrf_token": get_csrf_token(request),
        },
    )

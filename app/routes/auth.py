"""Authentication routes"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response


router = APIRouter()


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    """Logout by returning 401 to force browser to forget Basic Auth credentials"""
    # Check if this is a "confirmed" logout (user clicked button after seeing the page)
    confirmed = request.query_params.get("confirmed")

    if confirmed:
        # Return 401 to force browser to clear Basic Auth credentials
        response = Response(
            content="""
            <html>
            <head>
                <meta http-equiv="refresh" content="0;url=/login">
                <title>Logged Out</title>
            </head>
            <body>
                <p>You have been logged out. <a href="/login">Click here</a> if not redirected.</p>
            </body>
            </html>
            """,
            status_code=401,
            headers={"WWW-Authenticate": "Basic realm=\"LiveKit Dashboard\""},
            media_type="text/html"
        )
        return response

    # Show logout confirmation page
    return request.app.state.templates.TemplateResponse(
        "logout.html.j2",
        {
            "request": request,
        },
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page - redirects to home which triggers Basic Auth"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/", status_code=302)

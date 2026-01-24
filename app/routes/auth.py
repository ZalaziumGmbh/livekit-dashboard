"""Authentication routes"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response


router = APIRouter()


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    """Logout by returning 401 to force browser to forget Basic Auth credentials"""
    # Return 401 with a logout page - this clears Basic Auth credentials
    # The user must manually click the link to log back in
    return Response(
        content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logged Out - LiveKit Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card {
            background: #1e1e2f;
            border: 1px solid #2d2d44;
            max-width: 400px;
        }
        .card-body { color: #e0e0e0; }
        .text-muted { color: #8888aa !important; }
    </style>
</head>
<body>
    <div class="card">
        <div class="card-body text-center py-5">
            <i class="bi bi-check-circle text-success" style="font-size: 4rem;"></i>
            <h2 class="mt-3">Logged Out</h2>
            <p class="text-muted">You have been successfully logged out.</p>
            <p class="text-muted small">Your browser credentials have been cleared.</p>
            <a href="/" class="btn btn-primary mt-3">
                <i class="bi bi-box-arrow-in-right"></i> Log In Again
            </a>
        </div>
    </div>
</body>
</html>
        """,
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="LiveKit Dashboard"'},
        media_type="text/html"
    )

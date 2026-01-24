"""Authentication routes"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response


router = APIRouter()


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    """Logout by using JavaScript to clear Basic Auth credentials"""
    # The trick is to make the browser send a request with invalid credentials
    # This replaces the cached credentials with bad ones, effectively logging out
    return Response(
        content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logging Out - LiveKit Dashboard</title>
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
            <div id="logging-out">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h2 class="mt-3">Logging Out...</h2>
                <p class="text-muted">Please wait while we clear your session.</p>
            </div>
            <div id="logged-out" style="display: none;">
                <i class="bi bi-check-circle text-success" style="font-size: 4rem;"></i>
                <h2 class="mt-3">Logged Out</h2>
                <p class="text-muted">You have been successfully logged out.</p>
                <a href="/" class="btn btn-primary mt-3">
                    <i class="bi bi-box-arrow-in-right"></i> Log In Again
                </a>
            </div>
        </div>
    </div>
    <script>
        // Clear Basic Auth by making a request with invalid credentials
        // This replaces the browser's cached credentials
        (function() {
            try {
                // Method 1: Use XMLHttpRequest with wrong credentials
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '/_clear_auth', true, 'logout', 'logout');
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        showLoggedOut();
                    }
                };
                xhr.onerror = function() {
                    showLoggedOut();
                };
                xhr.send();

                // Fallback timeout in case request hangs
                setTimeout(showLoggedOut, 2000);
            } catch(e) {
                showLoggedOut();
            }

            function showLoggedOut() {
                document.getElementById('logging-out').style.display = 'none';
                document.getElementById('logged-out').style.display = 'block';
            }
        })();
    </script>
</body>
</html>
        """,
        status_code=200,
        media_type="text/html"
    )


@router.get("/_clear_auth")
async def clear_auth(request: Request):
    """Endpoint that always returns 401 to clear cached credentials"""
    return Response(
        content="Unauthorized",
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="LiveKit Dashboard"'},
        media_type="text/plain"
    )

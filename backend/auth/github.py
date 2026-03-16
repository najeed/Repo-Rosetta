from typing import Optional, Dict
import httpx
import os

class GitHubAuth:
    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET")

    async def get_access_token(self, code: str) -> Optional[str]:
        # Exchange OAuth code for access token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code
                },
                headers={"Accept": "application/json"}
            )
            if response.status_code == 200:
                return response.json().get("access_token")
        return None

    async def verify_permission(self, token: str, repo_full_name: str) -> bool:
        # Verify if user has >= Maintainer permission on the repo
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/repos/{repo_full_name}/collaborators/me/permission",
                headers={
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            if response.status_code == 200:
                permission = response.json().get("permission")
                return permission in ["admin", "maintainer"]
        return False

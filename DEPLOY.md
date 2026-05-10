# Deploying Traveloop via GHCR

Create a GitHub PAT with `write:packages` and `repo` scopes and add it to the repository secrets as `CR_PAT`.

On push to main/master the workflow publishes a Docker image to ghcr.io/<owner>/traveloop:latest.

To pull and run locally:
  docker pull ghcr.io/<owner>/traveloop:latest
  docker run -e DATABASE_URL="sqlite:///traveloop.db" -p 5000:5000 ghcr.io/<owner>/traveloop:latest

To deploy to any provider, point it to the ghcr image and set env vars (DATABASE_URL, SECRET_KEY, GITHUB_OAUTH_CLIENT_ID/SECRET).


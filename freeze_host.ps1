Write-Host "Freezing the host..." -ForegroundColor Cyan
gcloud run services update django-web-service `
  --region=europe-west1 `
  --max-instances=0
$PROJECT_ID = "my-django-portfolio"
$SERVICE_NAME = "django-web-service"
$REGION = "europe-west1"

Write-Host "1/3. Build Docker image in Google Cloud..." -ForegroundColor Green
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

Write-Host "2/3. Deploying container in Cloud Run..." -ForegroundColor Green
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --env-vars-file=.env

Write-Host "3/3. Updating Firebase Hosting configuration..." -ForegroundColor Green
firebase deploy --only hosting

Write-Host "Deployment completed successfully!" -ForegroundColor Cyan
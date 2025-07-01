# Deployment Guide

## Local Development

### Prerequisites
- **Node.js 16+** for React frontend
- **Python 3.8+** for FastAPI backend
- **npm or yarn** for package management

### Quick Start
```bash
# Option 1: Use start scripts
./start.sh          # Unix/Mac
start.bat           # Windows

# Option 2: Manual start
# Terminal 1: Backend
cd backend && pip install -r requirements.txt && python app.py

# Terminal 2: Frontend  
cd frontend && npm install && npm run dev
```

## Production Deployment

### Frontend (Static Hosting)

#### Vercel Deployment
```bash
cd frontend
npm run build
npx vercel --prod
```

#### Netlify Deployment
```bash
cd frontend
npm run build
# Drag dist/ folder to Netlify dashboard
```

#### GitHub Pages
```bash
cd frontend
npm run build
# Push dist/ contents to gh-pages branch
```

### Backend (API Hosting)

#### Railway Deployment
```bash
cd backend
# Add railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py"
  }
}
railway deploy
```

#### Heroku Deployment
```bash
cd backend
# Add Procfile
echo "web: python app.py" > Procfile
heroku create chatgpt-ui-demo-api
git push heroku main
```

#### Docker Deployment
```dockerfile
# backend/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["python", "app.py"]
```

```bash
docker build -t chatgpt-ui-demo-backend .
docker run -p 8001:8001 chatgpt-ui-demo-backend
```

## Environment Configuration

### Frontend Environment Variables
```bash
# frontend/.env.production
VITE_API_BASE_URL=https://your-api-domain.com/api
```

### Backend Environment Variables
```bash
# backend/.env
PORT=8001
CORS_ORIGINS=https://your-frontend-domain.com
DEBUG=false
```

## Domain & SSL Setup

### Custom Domain Configuration
1. **Frontend**: Configure DNS CNAME to hosting provider
2. **Backend**: Set up reverse proxy (nginx/CloudFlare)
3. **SSL**: Enable HTTPS (Let's Encrypt/CloudFlare)

### CORS Configuration
```python
# Update backend/app.py for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

## Performance Optimization

### Frontend Optimization
```bash
# Enable compression in vite.config.js
import { defineConfig } from 'vite'
import { gzip } from 'rollup-plugin-gzip'

export default defineConfig({
  plugins: [react(), gzip()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['chart.js', 'react-chartjs-2']
        }
      }
    }
  }
})
```

### Backend Optimization
```python
# Add caching headers
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## Monitoring & Analytics

### Error Tracking
```javascript
// Frontend: Add Sentry
import * as Sentry from "@sentry/react"
Sentry.init({ dsn: "YOUR_SENTRY_DSN" })
```

### Analytics
```html
<!-- Add Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
```

### Backend Monitoring
```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Security Hardening

### Production Security Checklist
- [ ] Enable HTTPS only
- [ ] Configure secure CORS policy
- [ ] Add rate limiting
- [ ] Implement input validation
- [ ] Add security headers
- [ ] Regular dependency updates
- [ ] Monitor for vulnerabilities

### Security Headers
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["your-domain.com", "*.your-domain.com"]
)
```

## Backup & Recovery

### Data Backup (if using real database)
```bash
# PostgreSQL backup
pg_dump -h localhost -U username dbname > backup.sql

# MongoDB backup  
mongodump --uri="mongodb://connection-string" --out backup/
```

### Rollback Strategy
1. Keep previous build artifacts
2. Use feature flags for gradual rollout
3. Database migration rollback scripts
4. CDN cache invalidation procedures

## Cost Optimization

### Free Tier Options
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Backend**: Railway, Render, Heroku (limited)
- **Database**: MongoDB Atlas, PlanetScale (when needed)
- **CDN**: CloudFlare (free tier)

### Scaling Considerations
- Start with serverless functions
- Add database only when persistence needed
- Use CDN for static assets
- Monitor usage and optimize accordingly 
# 🚀 Vercel Deployment Guide - Nada Records Techno Store

## 📋 Pre-deployment Checklist

### 1. Environment Variables Setup
Configure these environment variables in your Vercel dashboard:

#### Backend (Python/FastAPI)
```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# JWT Configuration  
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
SENDGRID_FROM_NAME=Nada Records

# Frontend URL
FRONTEND_URL=https://your-vercel-app.vercel.app

# Stripe (Optional)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Storage (Optional)
B2_KEY_ID=your-backblaze-key-id
B2_APPLICATION_KEY=your-backblaze-app-key
B2_BUCKET_NAME=your-bucket-name

# Application Settings
DEBUG=false
APP_NAME=Nada Records Techno Store API
APP_VERSION=1.0.0
```

#### Frontend (Next.js)
```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://your-vercel-app.vercel.app
NEXT_PUBLIC_FRONTEND_URL=https://your-vercel-app.vercel.app

# Stripe (Optional)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...

# Analytics (Optional)
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

### 2. Database Setup
1. **Create a PostgreSQL database** (recommended providers):
   - [Neon](https://neon.tech/) - Free tier available
   - [Supabase](https://supabase.com/) - Free tier available  
   - [Railway](https://railway.app/) - Free tier available
   - [Render](https://render.com/) - Free tier available

2. **Configure DATABASE_URL** in Vercel environment variables

### 3. Email Service Setup
1. **Create SendGrid account**: https://sendgrid.com/
2. **Generate API key** with Mail Send permissions
3. **Configure sender authentication** (domain or single sender)
4. **Add API key** to Vercel environment variables

## 🔧 Deployment Configuration

### Vercel Configuration Files

#### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    },
    {
      "src": "backend/vercel_main.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.11"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/backend/vercel_main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

#### Frontend `next.config.ts`
- ✅ API rewrites configured
- ✅ CORS headers set
- ✅ Audio file handling
- ✅ Environment variables mapped

#### Backend Requirements
- ✅ Simplified `requirements-vercel.txt` created
- ✅ `vercel_main.py` with limited dependencies
- ✅ Graceful degradation for missing features

## 🚀 Deployment Steps

### Option 1: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Option 2: GitHub Integration
1. **Connect your repository** to Vercel
2. **Configure build settings**:
   - Build Command: `npm run build`
   - Output Directory: `frontend/.next`
   - Install Command: `npm install`
3. **Add environment variables** in Vercel dashboard
4. **Deploy** automatically on push to main branch

### Option 3: Vercel Dashboard
1. **Import project** from Git repository
2. **Select framework preset**: Next.js
3. **Configure build settings** (auto-detected)
4. **Add environment variables**
5. **Deploy**

## 🔍 Post-Deployment Verification

### Health Checks
1. **Frontend**: https://your-app.vercel.app/
2. **API Health**: https://your-app.vercel.app/api/health
3. **Database**: https://your-app.vercel.app/api/v1/health/database
4. **Email**: https://your-app.vercel.app/api/v1/health/email

### API Endpoints
- ✅ **Authentication**: `/api/v1/auth/*`
- ✅ **Catalog**: `/api/v1/catalog/*`
- ⚠️ **Upload**: Limited on Vercel (file size restrictions)
- ✅ **Health**: `/api/v1/health/*`

## ⚠️ Vercel Limitations & Solutions

### File Upload Limitations
**Problem**: Vercel has a 4.5MB request limit
**Solution**: 
- Use external storage (AWS S3, Backblaze B2)
- Implement client-side chunked uploads
- Direct upload to storage from frontend

### Audio Processing Limitations  
**Problem**: Limited CPU time and memory
**Solution**:
- Move audio processing to external service
- Use background jobs with queue service
- Implement serverless audio processing

### WebSocket Limitations
**Problem**: Limited WebSocket support
**Solution**:
- Use Server-Sent Events (SSE) for real-time updates
- Implement polling for upload progress
- Use external WebSocket service

### Database Connection Limits
**Problem**: Serverless functions may exceed connection limits
**Solution**:
- Use connection pooling
- Implement connection caching
- Use database proxy services

## 🎯 Production Optimizations

### Performance
- ✅ **CDN**: Automatic via Vercel Edge Network
- ✅ **Compression**: Automatic gzip/brotli
- ✅ **Caching**: Configured for static assets
- ✅ **Image Optimization**: Next.js built-in

### Security
- ✅ **HTTPS**: Automatic SSL certificates
- ✅ **CORS**: Properly configured
- ✅ **Rate Limiting**: Implemented in API
- ✅ **Environment Variables**: Secure storage

### Monitoring
- ✅ **Error Tracking**: Built-in Vercel Analytics
- ✅ **Performance**: Web Vitals monitoring
- ✅ **Logs**: Function logs in dashboard
- ✅ **Health Checks**: Multiple endpoint monitoring

## 🐛 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check build logs in Vercel dashboard
# Common fixes:
- Update Node.js version in package.json engines
- Install missing dependencies
- Fix TypeScript errors
```

#### API Route Issues
```bash
# Verify API routes are accessible:
curl https://your-app.vercel.app/api/health

# Check environment variables are set
# Verify database connectivity
```

#### Import Errors
```bash
# Python import issues:
- Check PYTHONPATH is set correctly
- Verify all dependencies in requirements-vercel.txt
- Use simplified imports in vercel_main.py
```

#### Database Connection Issues
```bash
# Check DATABASE_URL format:
postgresql://username:password@host:port/database

# Verify database is accessible from Vercel
# Check connection limits and pooling
```

### Debug Commands
```bash
# Check deployment status
vercel inspect <deployment-url>

# View function logs
vercel logs <deployment-url>

# Test locally with Vercel dev
vercel dev
```

## 📱 Mobile & PWA Considerations

### Mobile Optimization
- ✅ **Responsive Design**: Tailwind CSS responsive utilities
- ✅ **Touch Interactions**: Mobile-friendly controls
- ✅ **Performance**: Optimized for mobile networks

### PWA Features (Future Enhancement)
- ⏳ **Service Worker**: For offline capabilities
- ⏳ **App Manifest**: For install prompts
- ⏳ **Push Notifications**: For user engagement

## 🔄 CI/CD Pipeline

### Automatic Deployments
- ✅ **Preview Deployments**: On pull requests
- ✅ **Production Deployments**: On main branch push
- ✅ **Environment Variables**: Per environment
- ✅ **Build Optimization**: Automatic caching

### Quality Gates
- ✅ **TypeScript**: Type checking
- ✅ **ESLint**: Code quality
- ✅ **Tests**: Unit and integration tests
- ✅ **Security**: Dependency scanning

## 📞 Support & Resources

### Documentation
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

### Community
- [Vercel Discord](https://discord.gg/vercel)
- [Next.js GitHub](https://github.com/vercel/next.js)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)

---

## 🎉 Success Checklist

- [ ] Environment variables configured
- [ ] Database connected and accessible
- [ ] Email service configured and tested
- [ ] Frontend loads without errors
- [ ] API health checks pass
- [ ] Authentication endpoints working
- [ ] Catalog endpoints returning data
- [ ] CORS properly configured
- [ ] SSL certificate active
- [ ] Performance metrics acceptable
- [ ] Error monitoring active

**Congratulations! Your Nada Records Techno Store is now live on Vercel! 🎵🚀**
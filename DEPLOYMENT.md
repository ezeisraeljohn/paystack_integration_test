# Deployment Guide - Paystack Payment Integration

This guide will help you deploy your Paystack payment integration platform to various hosting services.

## Prerequisites

Before deployment, ensure you have:

- ✅ Paystack account (test or live)
- ✅ API keys from Paystack dashboard
- ✅ Git repository (GitHub, GitLab, or Bitbucket)
- ✅ Code pushed to repository

## Option 1: Deploy to Render (Recommended - Free Tier Available)

### Steps:

1. **Sign up at [Render](https://render.com)**

2. **Create a New Web Service**

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the Service**

   - Name: `paystack-integration`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   Go to Environment section and add:

   ```
   PAYSTACK_SECRET_KEY=sk_test_your_secret_key
   PAYSTACK_PUBLIC_KEY=pk_test_your_public_key
   PAYSTACK_BASE_URL=https://api.paystack.co
   APP_URL=https://your-app-name.onrender.com
   DEBUG=False
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

### Configure Webhook in Paystack:

- Go to Paystack Dashboard → Settings → Webhooks
- Add: `https://your-app-name.onrender.com/webhook/paystack`

---

## Option 2: Deploy to Heroku

### Steps:

1. **Install Heroku CLI**

   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**

   ```bash
   heroku login
   ```

3. **Create a New App**

   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**

   ```bash
   heroku config:set PAYSTACK_SECRET_KEY=sk_test_your_key
   heroku config:set PAYSTACK_PUBLIC_KEY=pk_test_your_key
   heroku config:set PAYSTACK_BASE_URL=https://api.paystack.co
   heroku config:set APP_URL=https://your-app-name.herokuapp.com
   heroku config:set DEBUG=False
   ```

5. **Deploy**

   ```bash
   git push heroku main
   ```

6. **Open Your App**
   ```bash
   heroku open
   ```

### Configure Webhook:

- Webhook URL: `https://your-app-name.herokuapp.com/webhook/paystack`

---

## Option 3: Deploy to Railway

### Steps:

1. **Sign up at [Railway](https://railway.app)**

2. **Create New Project**

   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**
   In the Variables tab, add:

   ```
   PAYSTACK_SECRET_KEY=sk_test_your_key
   PAYSTACK_PUBLIC_KEY=pk_test_your_key
   PAYSTACK_BASE_URL=https://api.paystack.co
   APP_URL=https://your-app.up.railway.app
   DEBUG=False
   ```

4. **Deploy**
   - Railway automatically deploys
   - Get your URL from the deployment

### Configure Webhook:

- Webhook URL: `https://your-app.up.railway.app/webhook/paystack`

---

## Option 4: Deploy to Vercel

### Steps:

1. **Install Vercel CLI**

   ```bash
   npm install -g vercel
   ```

2. **Deploy**

   ```bash
   cd /home/ezeisraeljohn/paystack_integration_test
   vercel
   ```

3. **Follow prompts:**

   - Link to existing project or create new
   - Set up project
   - Deploy

4. **Add Environment Variables**

   ```bash
   vercel env add PAYSTACK_SECRET_KEY
   vercel env add PAYSTACK_PUBLIC_KEY
   vercel env add PAYSTACK_BASE_URL
   vercel env add APP_URL
   ```

5. **Redeploy with env vars**
   ```bash
   vercel --prod
   ```

### Configure Webhook:

- Webhook URL: `https://your-app.vercel.app/webhook/paystack`

---

## Option 5: Deploy to DigitalOcean App Platform

### Steps:

1. **Sign up at [DigitalOcean](https://digitalocean.com)**

2. **Create New App**

   - Go to App Platform
   - Click "Create App"
   - Connect GitHub repository

3. **Configure**

   - Detected as Python app
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn main:app --host 0.0.0.0 --port 8080`

4. **Environment Variables**
   Add in the Environment section:

   ```
   PAYSTACK_SECRET_KEY=sk_test_your_key
   PAYSTACK_PUBLIC_KEY=pk_test_your_key
   PAYSTACK_BASE_URL=https://api.paystack.co
   APP_URL=https://your-app.ondigitalocean.app
   DEBUG=False
   ```

5. **Deploy**
   - Click "Create Resources"
   - Wait for deployment

### Configure Webhook:

- Webhook URL: `https://your-app.ondigitalocean.app/webhook/paystack`

---

## Post-Deployment Checklist

After deploying to any platform:

### 1. Test the Application

- [ ] Visit your deployed URL
- [ ] Fill out payment form
- [ ] Complete a test payment using Paystack test cards
- [ ] Verify transaction appears in transactions page

### 2. Configure Paystack Webhook

- [ ] Go to Paystack Dashboard
- [ ] Navigate to Settings → Webhooks
- [ ] Add your webhook URL
- [ ] Test webhook delivery

### 3. Verify Environment Variables

- [ ] Check all env vars are set correctly
- [ ] Test API key authentication
- [ ] Ensure APP_URL matches your domain

### 4. Security Checks

- [ ] Confirm HTTPS is enabled
- [ ] Test webhook signature verification
- [ ] Verify secret keys are not exposed in logs
- [ ] Enable error monitoring

### 5. Monitor

- [ ] Check application logs
- [ ] Monitor webhook deliveries in Paystack dashboard
- [ ] Track successful payments
- [ ] Set up alerts for errors

---

## Testing with Test Cards

Use these Paystack test cards:

### Successful Payments:

```
Card Number: 4084 0840 8408 4081
CVV: 408
Expiry: Any future date
PIN: 0000
```

### Failed Payment:

```
Card Number: 5060 6666 6666 6666 4003
CVV: 123
Expiry: Any future date
```

---

## Troubleshooting

### Issue: Webhook not receiving events

**Solution:**

1. Check webhook URL is correct in Paystack dashboard
2. Ensure endpoint is accessible (test with curl)
3. Check application logs for errors
4. Verify signature verification is working

### Issue: Payment succeeds but transaction not updating

**Solution:**

1. Check webhook delivery in Paystack dashboard
2. Verify webhook signature verification
3. Check application logs
4. Test verify transaction API manually

### Issue: Environment variables not loading

**Solution:**

1. Verify .env file is not in .gitignore (it should be)
2. Set environment variables in hosting platform
3. Restart the application
4. Check variable names match exactly

### Issue: HTTPS errors

**Solution:**

1. Ensure deployment platform provides HTTPS
2. Update APP_URL to use https://
3. Test with curl to verify SSL certificate

---

## Monitoring & Maintenance

### Regular Tasks:

1. **Daily**: Check webhook delivery logs in Paystack
2. **Weekly**: Reconcile transactions with Paystack
3. **Monthly**: Review error logs and fix issues
4. **Quarterly**: Update dependencies

### Recommended Tools:

- **Logging**: LogDNA, Papertrail, or platform-native logs
- **Monitoring**: New Relic, Datadog, or Sentry
- **Uptime**: UptimeRobot or Pingdom
- **Analytics**: Google Analytics or Mixpanel

---

## Going Live (Production)

When ready for production:

1. **Get Live API Keys**

   - Go to Paystack Dashboard
   - Switch to Live mode
   - Copy live API keys

2. **Update Environment Variables**

   ```
   PAYSTACK_SECRET_KEY=sk_live_your_live_key
   PAYSTACK_PUBLIC_KEY=pk_live_your_live_key
   DEBUG=False
   ```

3. **Test Thoroughly**

   - Make real payment (small amount)
   - Verify webhook delivery
   - Test all flows

4. **Security Hardening**

   - Enable rate limiting
   - Add request validation
   - Implement comprehensive logging
   - Set up monitoring and alerts

5. **Compliance**
   - Add privacy policy
   - Add terms of service
   - Comply with PCI DSS if storing card data
   - Add GDPR compliance if serving EU customers

---

## Support

If you need help:

1. Check Paystack documentation: https://paystack.com/docs
2. Review application logs
3. Test endpoints with Postman
4. Contact Paystack support: support@paystack.com

---

**Congratulations! Your Paystack integration is now deployed!** 🎉

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv
import hmac
import hashlib
from datetime import datetime
from typing import Optional

# Load environment variables
load_dotenv()

app = FastAPI(title="Paystack Payment Integration", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Paystack Configuration
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")
PAYSTACK_BASE_URL = os.getenv("PAYSTACK_BASE_URL", "https://api.paystack.co")
APP_URL = os.getenv("APP_URL", "http://localhost:8000")

# In-memory storage for demo (use database in production)
transactions = {}
customers = {}


def get_paystack_headers():
    """Get headers for Paystack API requests"""
    return {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with payment form"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "public_key": PAYSTACK_PUBLIC_KEY,
            "app_url": APP_URL
        }
    )


@app.get("/transactions", response_class=HTMLResponse)
async def transactions_page(request: Request):
    """View all transactions"""
    return templates.TemplateResponse(
        "transactions.html",
        {
            "request": request,
            "transactions": list(transactions.values())
        }
    )


@app.post("/api/initialize-payment")
async def initialize_payment(
    email: str = Form(...),
    amount: float = Form(...),
    name: Optional[str] = Form(None)
):
    """
    API 1: Initialize Transaction
    Creates a new payment transaction and returns authorization URL
    """
    try:
        # Paystack expects amount in kobo (smallest currency unit)
        amount_in_kobo = int(amount * 100)
        
        # Prepare request payload
        payload = {
            "email": email,
            "amount": amount_in_kobo,
            "currency": "NGN",
            "callback_url": f"{APP_URL}/payment-callback",
            "metadata": {
                "customer_name": name or "Guest",
                "payment_date": datetime.now().isoformat()
            }
        }
        
        # Call Paystack Initialize Transaction API
        response = requests.post(
            f"{PAYSTACK_BASE_URL}/transaction/initialize",
            json=payload,
            headers=get_paystack_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["status"]:
                # Store transaction reference
                reference = data["data"]["reference"]
                transactions[reference] = {
                    "reference": reference,
                    "email": email,
                    "amount": amount,
                    "name": name or "Guest",
                    "status": "pending",
                    "created_at": datetime.now().isoformat()
                }
                
                return JSONResponse(content={
                    "status": True,
                    "message": "Transaction initialized successfully",
                    "data": data["data"]
                })
            else:
                raise HTTPException(status_code=400, detail=data.get("message", "Failed to initialize transaction"))
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to initialize payment")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/verify-payment/{reference}")
async def verify_payment(reference: str):
    """
    API 2: Verify Transaction
    Confirms if a transaction was successful
    """
    try:
        # Call Paystack Verify Transaction API
        response = requests.get(
            f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers=get_paystack_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data["status"]:
                transaction_data = data["data"]
                
                # Update local transaction record
                if reference in transactions:
                    transactions[reference]["status"] = transaction_data["status"]
                    transactions[reference]["verified_at"] = datetime.now().isoformat()
                    transactions[reference]["gateway_response"] = transaction_data.get("gateway_response")
                    transactions[reference]["paid_at"] = transaction_data.get("paid_at")
                    transactions[reference]["channel"] = transaction_data.get("channel")
                
                return JSONResponse(content={
                    "status": True,
                    "message": "Verification successful",
                    "data": {
                        "reference": reference,
                        "amount": transaction_data["amount"] / 100,  # Convert from kobo
                        "status": transaction_data["status"],
                        "paid_at": transaction_data.get("paid_at"),
                        "channel": transaction_data.get("channel"),
                        "currency": transaction_data.get("currency"),
                        "customer": transaction_data.get("customer", {}).get("email")
                    }
                })
            else:
                raise HTTPException(status_code=400, detail="Verification failed")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to verify payment")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/list-transactions")
async def list_transactions(page: int = 1, perPage: int = 10):
    """
    API 3: List Transactions (Bonus API)
    Fetches list of transactions from Paystack
    """
    try:
        params = {
            "page": page,
            "perPage": perPage
        }
        
        response = requests.get(
            f"{PAYSTACK_BASE_URL}/transaction",
            headers=get_paystack_headers(),
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data["status"]:
                # Format transactions
                formatted_transactions = []
                for txn in data["data"]:
                    formatted_transactions.append({
                        "reference": txn.get("reference"),
                        "amount": txn.get("amount", 0) / 100,
                        "email": txn.get("customer", {}).get("email"),
                        "status": txn.get("status"),
                        "paid_at": txn.get("paid_at"),
                        "channel": txn.get("channel"),
                        "currency": txn.get("currency")
                    })
                
                return JSONResponse(content={
                    "status": True,
                    "message": "Transactions retrieved successfully",
                    "data": formatted_transactions,
                    "meta": data.get("meta", {})
                })
            else:
                raise HTTPException(status_code=400, detail="Failed to fetch transactions")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch transactions")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook/paystack")
async def paystack_webhook(request: Request):
    """
    Webhook endpoint to receive payment notifications from Paystack
    This demonstrates real-time payment status updates
    """
    try:
        # Get the signature from headers
        signature = request.headers.get("x-paystack-signature")
        
        # Get the raw body
        body = await request.body()
        
        # Verify webhook signature
        if signature:
            hash_value = hmac.new(
                PAYSTACK_SECRET_KEY.encode('utf-8'),
                body,
                hashlib.sha512
            ).hexdigest()
            
            if hash_value != signature:
                raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Parse the webhook data
        event = await request.json()
        
        # Handle different event types
        event_type = event.get("event")
        
        if event_type == "charge.success":
            # Payment was successful
            data = event.get("data", {})
            reference = data.get("reference")
            
            if reference in transactions:
                transactions[reference]["status"] = "success"
                transactions[reference]["webhook_received_at"] = datetime.now().isoformat()
                transactions[reference]["amount_paid"] = data.get("amount", 0) / 100
        
        return JSONResponse(content={"status": "success"})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/payment-callback", response_class=HTMLResponse)
async def payment_callback(request: Request, reference: str = None):
    """Payment callback page after Paystack redirect"""
    return templates.TemplateResponse(
        "callback.html",
        {
            "request": request,
            "reference": reference
        }
    )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Paystack Payment Integration",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

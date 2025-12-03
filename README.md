# Paystack Payment Integration Demo

A comprehensive payment integration platform built with FastAPI that demonstrates the implementation of Paystack APIs with a modern, user-friendly interface.

## 🚀 Features

- **Payment Initialization**: Initialize transactions using Paystack's Transaction Initialize API
- **Payment Verification**: Verify completed transactions using Paystack's Transaction Verify API
- **Transaction Listing**: View all transactions with pagination support
- **Webhook Support**: Handle real-time payment notifications from Paystack
- **Modern UI**: Beautiful, responsive interface built with Bootstrap 5
- **Secure**: Implements proper API authentication and webhook signature verification

## 📋 Implemented Paystack APIs

### 1. Initialize Transaction API

- **Endpoint**: `POST /transaction/initialize`
- **Purpose**: Creates a new payment transaction and returns an authorization URL
- **Implementation**: `POST /api/initialize-payment`

### 2. Verify Transaction API

- **Endpoint**: `GET /transaction/verify/:reference`
- **Purpose**: Confirms if a transaction was successful
- **Implementation**: `GET /api/verify-payment/{reference}`

### 3. List Transactions API (Bonus)

- **Endpoint**: `GET /transaction`
- **Purpose**: Fetches a paginated list of all transactions
- **Implementation**: `GET /api/list-transactions`

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Payment Gateway**: Paystack
- **Templating**: Jinja2
- **Deployment**: Docker, Docker Compose

## 🐳 Quick Start with Docker (Recommended)

The fastest way to get started!

### Using Make (Simplest)

```bash
# Build and run in one command
make deploy

# Or step by step
make build
make run
```

### Using Docker directly

```bash
# Build the image
docker build -t paystack-app .

# Run the container
docker run -d -p 8000:8000 --env-file .env --name paystack-app paystack-app

# View at http://localhost:8000
```

### Using Docker Compose

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**📚 Full Docker guide:** See [DOCKER.md](DOCKER.md) for complete deployment options

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Paystack account (test or live)

### Setup Instructions

1. **Clone or navigate to the repository**

   ```bash
   cd /home/ezeisraeljohn/paystack_integration_test
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Copy `.env.example` to `.env`
   - Update the `.env` file with your Paystack API keys:

   ```env
   PAYSTACK_SECRET_KEY=sk_test_your_secret_key
   PAYSTACK_PUBLIC_KEY=pk_test_your_public_key
   PAYSTACK_BASE_URL=https://api.paystack.co
   APP_URL=http://localhost:8000
   DEBUG=True
   ```

5. **Get your Paystack API keys**

   - Sign up at [Paystack](https://paystack.com)
   - Navigate to Settings > API Keys & Webhooks
   - Copy your test keys

6. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

7. **Access the application**
   - Open your browser and visit: http://localhost:8000

## 🎯 Usage

### Making a Payment

1. Navigate to the home page (http://localhost:8000)
2. Fill in the payment form:
   - Full Name
   - Email Address
   - Amount (in NGN)
3. Click "Pay Now"
4. Complete the payment in the Paystack popup
5. You'll be redirected to a confirmation page

### Viewing Transactions

1. Click "Transactions" in the navigation menu
2. View all processed transactions
3. Click "View" on any transaction to see details
4. Click "Refresh" to reload the transaction list

### Testing Payments

Use Paystack's test cards:

- **Successful Payment**: 4084 0840 8408 4081 (CVV: 408, Expiry: any future date)
- **Declined Payment**: 5060 6666 6666 6666 4003

## 📡 API Endpoints

### Frontend Routes

- `GET /` - Home page with payment form
- `GET /transactions` - Transaction history page
- `GET /payment-callback` - Payment callback page

### Backend API Routes

- `POST /api/initialize-payment` - Initialize a new payment
- `GET /api/verify-payment/{reference}` - Verify a transaction
- `GET /api/list-transactions` - List all transactions
- `POST /webhook/paystack` - Webhook endpoint for Paystack
- `GET /api/health` - Health check endpoint

## 🔐 Security Features

- API key authentication for Paystack requests
- Webhook signature verification using HMAC SHA512
- Environment variable configuration
- HTTPS support (recommended for production)

## 📝 Section 2 Questions - Answers

### Q1: Did you encounter any issues when using the Paystack APIs and how did you resolve them?

**Issues Encountered:**

1. **Authentication Errors**

   - **Issue**: Initially received 401 Unauthorized errors
   - **Resolution**: Ensured the Authorization header format was correct: `Bearer {secret_key}`. Also verified that the secret key was properly loaded from environment variables.

2. **Amount Format Confusion**

   - **Issue**: Payments were failing because amounts were in the wrong format
   - **Resolution**: Learned that Paystack expects amounts in kobo (smallest currency unit). Implemented conversion: `amount_in_kobo = amount * 100`.

3. **Webhook Signature Verification**

   - **Issue**: Webhook requests were being rejected initially
   - **Resolution**: Implemented proper HMAC SHA512 signature verification using the secret key to validate webhook authenticity.

4. **CORS Issues During Development**

   - **Issue**: Browser blocking requests due to CORS policy
   - **Resolution**: Used Paystack's popup/inline.js library which handles this automatically. For API testing, used proper headers and considered CORS middleware.

5. **Reference Collision**
   - **Issue**: Duplicate transaction references causing errors
   - **Resolution**: Let Paystack generate unique references automatically or implement UUID-based reference generation.

### Q2: How can you confirm if a transaction was successful or not?

**Multiple Methods to Confirm Transaction Success:**

1. **Verify Transaction API (Primary Method)**

   ```python
   GET /transaction/verify/:reference
   ```

   - Most reliable method
   - Checks transaction status directly from Paystack
   - Returns detailed transaction information including:
     - Status (success, failed, abandoned)
     - Amount paid
     - Payment channel used
     - Customer details
     - Transaction timestamp

2. **Webhook Notifications (Recommended)**

   - Paystack sends real-time webhook events to your server
   - Listen for `charge.success` event
   - Verify webhook signature for security
   - Update your database immediately
   - Most efficient for production systems

3. **Transaction Status Codes**

   - `success` - Payment completed successfully
   - `failed` - Payment failed
   - `abandoned` - Customer didn't complete payment
   - `pending` - Payment in progress

4. **Response from Initialize Transaction**
   - Initial response contains authorization URL
   - After payment, Paystack redirects to callback URL with reference
   - Use reference to verify the transaction

**Best Practice Implementation:**

```python
# 1. Customer completes payment
# 2. Receive webhook notification (instant)
# 3. Verify transaction using Verify API (confirmation)
# 4. Update order status in database
# 5. Send confirmation email to customer
```

**Code Example:**

```python
async def verify_payment(reference: str):
    response = requests.get(
        f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
        headers={"Authorization": f"Bearer {SECRET_KEY}"}
    )
    data = response.json()

    if data["status"] and data["data"]["status"] == "success":
        # Payment successful
        amount = data["data"]["amount"] / 100  # Convert from kobo
        return True, amount
    else:
        # Payment failed or pending
        return False, None
```

### Q3: What are webhooks?

**Comprehensive Explanation:**

**Definition:**
Webhooks are automated HTTP callbacks that enable real-time communication between applications. When a specific event occurs in one system (like Paystack), it automatically sends data to a predefined URL in your application.

**How Webhooks Work:**

1. **Setup**

   - You configure a webhook URL in Paystack dashboard (e.g., `https://yourapp.com/webhook/paystack`)
   - Choose which events to listen for (charge.success, transfer.success, etc.)

2. **Event Occurs**

   - Customer completes a payment
   - Paystack processes the transaction

3. **Webhook Triggered**

   - Paystack immediately sends an HTTP POST request to your webhook URL
   - Request contains event data (transaction details, customer info, etc.)

4. **Your Server Responds**
   - Receives and validates the webhook
   - Processes the data (update database, send emails, etc.)
   - Returns 200 OK response to acknowledge receipt

**Webhooks vs Polling:**

| Webhooks (Push)          | Polling (Pull)                  |
| ------------------------ | ------------------------------- |
| Real-time updates        | Delayed updates                 |
| Efficient (event-driven) | Inefficient (constant checking) |
| No unnecessary requests  | Many wasted requests            |
| Instant notification     | Check intervals (every 5 min)   |

**Paystack Webhook Events:**

- `charge.success` - Successful payment
- `charge.failed` - Failed payment
- `transfer.success` - Successful transfer
- `transfer.failed` - Failed transfer
- And many more...

**Security Considerations:**

1. **Signature Verification**

   ```python
   def verify_webhook_signature(payload, signature, secret):
       hash_value = hmac.new(
           secret.encode('utf-8'),
           payload,
           hashlib.sha512
       ).hexdigest()
       return hash_value == signature
   ```

2. **HTTPS Only**: Always use HTTPS for webhook URLs
3. **Validate Event Data**: Check all data before processing
4. **Idempotency**: Handle duplicate webhook events gracefully

**Benefits of Webhooks:**

- ⚡ **Real-time**: Instant updates when events occur
- 🎯 **Efficient**: No need for constant polling
- 🔄 **Automatic**: No manual intervention required
- 📊 **Reliable**: Paystack retries failed webhooks
- 💰 **Cost-effective**: Reduces API calls and server load

**Implementation in This Project:**

```python
@app.post("/webhook/paystack")
async def paystack_webhook(request: Request):
    # Get signature
    signature = request.headers.get("x-paystack-signature")

    # Get payload
    body = await request.body()

    # Verify signature
    if not verify_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Process event
    event = await request.json()
    if event["event"] == "charge.success":
        # Update transaction status
        reference = event["data"]["reference"]
        update_transaction_status(reference, "success")

    return {"status": "success"}
```

## 🚀 Deployment

### Deployment Options

1. **Heroku**

   ```bash
   heroku create your-app-name
   git push heroku main
   heroku config:set PAYSTACK_SECRET_KEY=your_key
   ```

2. **Vercel**

   ```bash
   vercel deploy
   ```

3. **Railway**

   ```bash
   railway deploy
   ```

4. **DigitalOcean/AWS/GCP**
   - Use Docker for containerization
   - Set up CI/CD pipeline
   - Configure environment variables

### Procfile (for Heroku)

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Runtime.txt (for Heroku)

```
python-3.12.3
```

## 📚 Project Structure

```
paystack_integration_test/
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables
├── .env.example                    # Environment template
├── create_section1_answers.py      # Script to generate Section 1 doc
├── Section_1_Answers.docx          # Section 1 answers
├── README.md                       # This file
├── Procfile                        # Heroku deployment config
├── templates/
│   ├── index.html                  # Home page
│   ├── transactions.html           # Transactions page
│   └── callback.html              # Payment callback page
└── static/
    └── style.css                   # Additional styles
```

## 🧪 Testing

### Manual Testing

1. **Test Payment Flow**

   - Use test cards from Paystack
   - Verify transaction appears in dashboard
   - Check webhook delivery in Paystack dashboard

2. **Test Verification**

   - Copy transaction reference
   - Call verify endpoint
   - Confirm status matches

3. **Test Error Handling**
   - Use declined test card
   - Cancel payment popup
   - Verify error messages display correctly

### API Testing with curl

```bash
# Initialize Payment
curl -X POST http://localhost:8000/api/initialize-payment \
  -F "email=test@example.com" \
  -F "amount=1000" \
  -F "name=Test User"

# Verify Payment
curl http://localhost:8000/api/verify-payment/REFERENCE_HERE

# List Transactions
curl http://localhost:8000/api/list-transactions
```

## 🤝 Contributing

This is a technical assessment project. For production use, consider:

- Adding database integration (PostgreSQL, MongoDB)
- Implementing user authentication
- Adding comprehensive error handling
- Setting up logging and monitoring
- Implementing rate limiting
- Adding unit and integration tests

## 📄 License

This project is created for educational and assessment purposes.

## 👤 Author

Israel Eze

- Technical Support Specialist Assessment Project
- Paystack API Integration Demo

## 🙏 Acknowledgments

- [Paystack](https://paystack.com) for their excellent API documentation
- [FastAPI](https://fastapi.tiangolo.com) for the amazing web framework
- [Bootstrap](https://getbootstrap.com) for the UI components

## 📞 Support

For issues or questions:

1. Check Paystack documentation: https://paystack.com/docs/api/
2. Review this README
3. Check application logs
4. Contact support if needed

---

**Note**: This is a demo application. For production deployment, ensure you:

- Use production API keys
- Enable HTTPS
- Implement proper database
- Add comprehensive logging
- Set up monitoring and alerts
- Follow security best practices

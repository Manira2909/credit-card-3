# Credit Card Payment System

## Database Setup
Create MySQL DB : 'credit_card_db'
Copy '.env.example' to '.env'
Update password: 'Manira2909*'
Run backend - tables auto-create

## Setup
Backend: pip install -r requirements.txt && uvicorn app.main:app --reload
Frontend: npm install && npm run dev

## Admin Credentials
admin@test.com / Admin@123
test@test.com / 123456

## Security Features
- JWT Auth, bcrypt passwords, No CVV storage, Luhn validation, Encrypted cards
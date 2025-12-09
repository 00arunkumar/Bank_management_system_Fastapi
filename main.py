from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Bank API")


#-------------------------------
# in-memory database
#-----------------------------------

customers = {}
accounts = {}

customer_id_counter = 1
account_id_counter = 1


#----------------------------
# Request Models
#-----------------------------

class CustomerCreate(BaseModel):
    name: str


class AccountCreate(BaseModel):
    customer_id: int


class Transaction(BaseModel):
    account_id: int
    amount: float




#------------------------------
# Endpoints
#-------------------------------

@app.post("/customer")
def create_customer(customer: CustomerCreate):
    global customer_id_counter
    customers[customer_id_counter] = {
        "id": customer_id_counter,
        "name": customer.name
    }
    customer_id_counter += 1
    return {"message": "Customer created", "customer": customers[customer_id_counter - 1]}


@app.post("/account")
def create_account(acc: AccountCreate):
    global account_id_counter

    if acc.customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    

    accounts[account_id_counter] = {
        "id": account_id_counter,
        "customer_id": acc.customer_id,
        "balance": 0.0
    }

    account_id_counter += 1
    return {"message": "Account created", "account": accounts[account_id_counter - 1]}


@app.post("/deposit")
def deposit_money(tx: Transaction):
    if tx.account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    accounts[tx.account_id]["balance"] += tx.amount
    return{
        "message": "Deposit successful",
        "new_balance": accounts[tx.account_id]["balance"]
    }


@app.post("/withdraw")
def withdraw_money(tx: Transaction):
    if tx.account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if accounts[tx.account_id]["balance"] < tx.amount:
        raise HTTPException(status_code=404, detail="Insufficient balance")
    
    accounts[tx.account_id]["balance"] -= tx.amount
    return {
        "message": "Withdrawal successful",
        "new_balance": accounts[tx.account_id]["balance"]
    }


@app.get("/balance/{account_id}")
def get_balance(account_id: int):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return {"account_id": account_id, "balance": accounts[account_id]['balance']}
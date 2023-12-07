from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from sqlalchemy.orm import Session
from schemas import expense as expense_schemas
from models import expense
from db.database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/expenses",
    tags=['Expenses']
)


@router.get('/', response_model=List[expense_schemas.ShowExpense], status_code=status.HTTP_200_OK)
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(expense.Expense).all()

    return expenses


@router.get('/user-expenses', response_model=List[expense_schemas.ShowExpense], status_code=status.HTTP_200_OK)
def get_user_expenses(user_id: str, db: Session = Depends(get_db)):
    expenses = db.query(expense.Expense).filter(
        expense.Expense.user_id == user_id).all()

    return expenses


@router.get('/{id}', response_model=expense_schemas.ShowExpense, status_code=status.HTTP_200_OK)
def get_expense(id: str, db: Session = Depends(get_db)):
    single_expense = db.query(expense.Expense).filter(
        expense.Expense.id == id).first()

    if not single_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Expense with id of {id} does not exist.")

    return single_expense


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_expense(request: expense_schemas.ExpenseSchema, db: Session = Depends(get_db)):
    new_expense = expense.Expense(user_id=request.user_id, merchant=request.merchant, date=request.date, total=request.total,
                                  currency=request.currency, category=request.category, description=request.description, receipt=request.receipt)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_expense(id: str, request: expense_schemas.UpdateExpenseSchema, db: Session = Depends(get_db)):
    single_expense = db.query(expense.Expense).filter(expense.Expense.id == id)
    if not single_expense.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Expense with id of {id} does not exist.")

    single_expense.update({'user_id': request.user_id, 'merchant': request.merchant, 'date': request.date, 'total': request.total,
                           'currency': request.currency, 'category': request.category, 'description': request.description, 'receipt': request.receipt,
                           'expense_stage': request.expense_stage,
                           })
    db.commit()
    
    return "Updated"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from models import expense, user, supportTicket, profile, notification, newsLetterList
from routers import expense as expense_router, user as user_router, authentication as authentication_router, supportTicket as support_ticket_router, profile as profile_router, notification as notification_router, news_letter_list as news_letter_list_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

expense.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
supportTicket.Base.metadata.create_all(bind=engine)
profile.Base.metadata.create_all(bind=engine)
notification.Base.metadata.create_all(bind=engine)
newsLetterList.Base.metadata.create_all(bind=engine)

# Routers
app.include_router(user_router.router)
app.include_router(authentication_router.router)
app.include_router(profile_router.router)
app.include_router(expense_router.router)
app.include_router(support_ticket_router.router)
app.include_router(notification_router.router)
app.include_router(news_letter_list_router.router)

from loguru import logger
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from starlette import status
from jwtserver.api.v1.help_func.ParseToken import TokenProcessor
from jwtserver.api.v1.help_func.recaptcha import RecaptchaV3
from jwtserver.app import app
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Response, HTTPException, Body
from jwtserver.functions.secure import verify_password
from jwtserver.functions.session_db import async_db_session
from jwtserver.models import User
from jwtserver.functions.config import load_config

config = load_config().token


@app.post("/api/v1/auth/login/")
async def login(
        response: Response,
        telephone: str = Body(...),
        password: str = Body(...),
        session: AsyncSession = Depends(async_db_session),
        recaptcha: RecaptchaV3 = Depends(RecaptchaV3)
):
    logger.debug(telephone, password)
    await recaptcha.set_action_name('LoginPage/LoginButton').greenlight()
    stmt = select(User).where(User.telephone == telephone)
    result = await session.execute(stmt)
    try:
        user = result.scalars().one()
        logger.debug(user)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный номер или пароль",
            headers={"WWW-Authenticate": "JSv1"},
        )

    if verify_password(password, user.password):
        token_processor = TokenProcessor()
        logger.debug(token_processor)
        access_token, refresh_token = token_processor.create_pair_tokens(user.uuid.hex)
        logger.debug(access_token, refresh_token)
        logger.debug(access_token, refresh_token)
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            max_age=config.refresh_expire_time * 60)

        logger.debug({"access_token": access_token, "token_type": "JSv1"})
        return {"access_token": access_token, "token_type": "JSv1"}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный номер или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

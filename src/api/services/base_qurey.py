from sqlalchemy import select, Result, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.setup_logger import logger


class BaseQuery:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    @logger
    async def get_all_fields(self) -> Result:
        """
        Получить список всех полей объекта
        :return: Result
        """
        result = await self.session.execute(select(self.model))
        return result

    @logger
    async def get_object_by_kwargs(self, **kwargs) -> Result:
        """
        Получить объект или объекты по параметрам
        :param kwargs: параметры для поиска, например "id=1", "status='open'"
        :return: Result
        """
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if not filtered_kwargs:
            return await self.get_all_fields()

        conditions = [
            getattr(self.model, key) == value for key, value in filtered_kwargs.items()
        ]
        query = select(self.model).where(*conditions)
        result = await self.session.execute(query)
        return result

    @logger
    async def update_object_by_kwargs(self, update_data: dict, **kwargs) -> Result:
        """
        Обновить объекты по заданным параметрам и вернуть обновлённые записи
        :param update_data: словарь с обновляемыми полями и их новыми значениями, например {"status": "closed"}
        :param kwargs: параметры для поиска (фильтрации), например "id=1", "status='open'"
        :return: Result - результат SELECT запроса на обновлённые объекты
        """

        filtered_update_data = {k: v for k, v in update_data.items() if v is not None}

        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if not filtered_kwargs:
            raise ValueError("Нельзя обновить объекты без указания фильтров (kwargs).")

        if not filtered_update_data:
            where_conditions = [
                getattr(self.model, key) == value
                for key, value in filtered_kwargs.items()
            ]
            query = select(self.model).where(*where_conditions)
            return await self.session.execute(query)

        where_conditions = [
            getattr(self.model, key) == value for key, value in filtered_kwargs.items()
        ]

        stmt = (
            update(self.model).where(*where_conditions).values(**filtered_update_data)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        select_query = select(self.model).where(*where_conditions)
        result = await self.session.execute(select_query)
        return result

    @logger
    async def create_object(self, **kwargs) -> object:
        """
        Создать новый объект модели
        :param kwargs: атрибуты объекта, например "description='...', "source='...'"
        :return: созданный объект модели
        """

        new_object = self.model(**kwargs)
        self.session.add(new_object)
        await self.session.commit()
        await self.session.refresh(new_object)
        return new_object

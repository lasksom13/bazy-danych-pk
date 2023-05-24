from abc import ABC, abstractmethod
import typing as tp

class BaseCommands(ABC):
    @abstractmethod
    def start_database(
            self
    ) -> None:
        pass

    @abstractmethod
    def create_table(
            self,
            table_name: str = "imdbdata"
    ) -> None:
        pass

    @abstractmethod
    def drop_table(
            self,
            table_name: str = "imdbdata"
    ) -> None:
        pass

    @abstractmethod
    def test_time_for_insert(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata",
            values: tp.Optional[tp.List] = None
    ) -> float:
        pass

    @abstractmethod
    def test_time_for_modify(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata"
    ) -> float:
        pass

    @abstractmethod
    def test_time_for_delete(
            self,
            record_amount: int = 10000,
            table_name: str = "imdbdata"
    ) -> float:
        pass

    @abstractmethod
    def get_record_amount(
            self,
            table_name: str = "imdbdata",
    ) -> int:
        pass

    @abstractmethod
    def test_time_for_record_amount_with_word(
            self,
            field_name: str,
            search_word: str,
            table_name: str = "imdbdata"
    ) -> float:
        pass






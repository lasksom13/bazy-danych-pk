from abc import ABC, abstractmethod


class BaseCommands(ABC):
    @abstractmethod
    def start_database(
            self
    ) -> None:
        pass

    @abstractmethod
    def create_table(
            self
    ) -> None:
        pass

    @abstractmethod
    def drop_table(
            self,
            table_name: str
    ) -> None:
        pass

    @abstractmethod
    def test_time_for_insert(
            self,
            record_amount: int,
            table_name: str
    ) -> float:
        pass

    @abstractmethod
    def test_time_for_modify(
            self,
            record_amount: int,
            table_name: str
    ) -> float:
        pass

    @abstractmethod
    def test_time_for_delete(
            self,
            record_amount: int,
            table_name: str
    ) -> float:
        pass

    @abstractmethod
    def get_record_amount(
            self,
            table_name: str
    ) -> int:
        pass

    @abstractmethod
    def test_time_for_record_amount_with_word(
            self,
            table_name: str,
            field_name: str,
            search_word: str
    ) -> float:
        pass






from abc import ABC, abstractmethod
from typing import Dict, Any
import io
import yaml

class CurrenciesProvider(ABC):
    '''  
    Интерфейс для поставщика валют.
    '''
    
    @abstractmethod
    def get_currencies(self) -> Dict[str, Any]:
        """
        Получить данные о валютах.

        Returns:
            Dict[str, Any]: Данные в виде словаря.
        """
        pass
    
    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """
        Сохранить данные в файл.

        Args:
            filename (str): Имя файла для сохранения.
        """
        pass


class CurrenciesProviderJSON(CurrenciesProvider):
    """
    Базовая реализация поставщика валют.
    Получает данные в формате JSON с сайта Центрального банка РФ.
    """
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    
    def get_currencies(self) -> Dict[str, Any]:
        """
        Выполнить HTTP-запрос и вернуть данные в формате JSON.

        Returns:
            Dict[str, Any]: Полученные данные.
        """
        import requests 
        
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()
    
    def save_to_file(self, filename: str) -> None:
        """
        Сохранить JSON-данные в файл.

        Args:
            filename (str): Имя файла для сохранения.
        """
        import json
        
        data = self.get_currencies()
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class CurrenciesDecorator(CurrenciesProvider):
    """
    Базовый декоратор для поставщиков валют.
    Позволяет расширять функциональность без изменения исходного класса.
    """
    _provider: CurrenciesProvider = None

    def __init__(self, provider: CurrenciesProvider) -> None:
        """
        Инициализация декоратора.

        Args:
            provider (CurrenciesProvider): Оборачиваемый объект.
        """
        self._provider = provider

    @property
    def provider(self) -> CurrenciesProvider:
        """
        Получить оборачиваемый объект.

        Returns:
            CurrenciesProvider: Оборачиваемый поставщик.
        """
        return self._provider

    def get_currencies(self) -> Dict[str, Any]:
        """
        Делегировать получение данных оборачиваемому объекту.

        Returns:
            Dict[str, Any]: Данные о валютах.
        """
        return self._provider.get_currencies()
    
    def save_to_file(self, filename: str) -> None:
        """
        Делегировать сохранение данных оборачиваемому объекту.

        Args:
            filename (str): Имя файла.
        """
        self._provider.save_to_file(filename)


class CSVDecorator(CurrenciesDecorator):
    """
    Декоратор, преобразующий данные о валютах в формат CSV.
    """
    def get_currencies(self) -> Dict[str, Any]:
        """
        Преобразовать данные JSON в текст CSV.

        Returns:
            Dict[str, Any]: Словарь с CSV-представлением данных.
        """
        import csv 
        
        data = self.provider.get_currencies()
        valutes = data["Valute"]

        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=["CharCode", "Name", "Nominal", "Value", "Previous"]
        )
        writer.writeheader()

        for info in valutes.values():
            writer.writerow({
                "CharCode": info["CharCode"],
                "Name": info["Name"],
                "Nominal": info["Nominal"],
                "Value": info["Value"],
                "Previous": info.get("Previous")
            })

        return {
            "format": "csv",
            "csv_text": output.getvalue()
        }
        
    def save_to_file(self, filename: str) -> None:
        """
        Сохранить данные в формате CSV в файл.

        Args:
            filename (str): Имя файла.
        """
        data = self.get_currencies()
        with open(filename, "w", encoding="utf-8", newline="") as file:
            file.write(data["csv_text"])


class YAMLDecorator(CurrenciesDecorator):
    """
    Декоратор, преобразующий данные о валютах в формат YAML.
    """
    def get_currencies(self) -> Dict[str, Any]:
        """
        Преобразовать данные JSON в текст YAML.

        Returns:
            Dict[str, Any]: Словарь с YAML-представлением данных.
        """
    
        data = self.provider.get_currencies()
        yaml_text = yaml.dump(data, allow_unicode=True, sort_keys=False)
        return {
            "format": "yaml",
            "yaml_text": yaml_text
        }
    
    def save_to_file(self, filename: str) -> None:
        """
        Сохранить данные в формате YAML в файл.

        Args:
            filename (str): Имя файла.
        """
        data = self.get_currencies()
        with open(filename, "w", encoding="utf-8") as file:
            file.write(data["yaml_text"])
            
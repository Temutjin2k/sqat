@smoke
Feature: Поиск билетов (Data Driven)

  Scenario: Поиск с использованием Excel
    Given я загружаю тестовые данные из Excel "data.xlsx" (строка 2)
    And я открываю сайт Aviasales
    When я ищу билет используя данные из Excel
    Then я вижу список результатов

  @smoke
  Scenario: Поиск по популярному направлению (Хардкод)
    Given я открываю сайт Aviasales
    When я ищу билет из "Алматы" в "Шымкент"
    Then я вижу список результатов
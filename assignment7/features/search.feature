@smoke
Feature: Ticket Search (Data Driven)

  Scenario: Search using Excel
    Given I load test data from Excel "data.xlsx" (row 2)
    And I open the Aviasales website
    When I search for a ticket using data from Excel
    Then I see a list of results

  @smoke
  Scenario: Search for a popular destination
    Given I open the Aviasales website
    When I search for a ticket from "Астана" to "Уральск"
    Then I see a list of results
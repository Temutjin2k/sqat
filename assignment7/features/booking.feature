@regression
Feature: Booking using data from Excel

  Scenario: Complete passenger form filling
    Given I load test data from Excel "data.xlsx" (row 2)
    And I have reached the booking page with data from Excel
    
    When I fill in contact details from Excel
    And I fill in passenger details from Excel
    And I fill in passport details from Excel
    Then I successfully select the Comfort package

  Scenario: Verify navigation to the booking page
    Given I have already found tickets from "Астана" to "Уральск"
    When I select the first ticket and click buy
    Then the booking tab opens
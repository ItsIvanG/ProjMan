*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Browser    https://www.facebook.com    chrome
Suite Teardown    Close Browser

*** Test Cases ***
Test Case 1: Dummy User Posts Status Publicly
    [Documentation]    Dummy user logs in and posts a status publicly
    Input Credentials
    Wait For Page To Load
    Post Status

Test Case 2: Dummy User Sends Message
    [Documentation]    Dummy user sends a message to your profile
    Input Credentials
    Wait For Page To Load
    Create Message    Lucas Kean
    Send Message    Hello world 2024! Hello Robot Framework!

*** Test Cases ***
Test Case 3: Send Multiple Messages With Delay
    [Documentation]    Sends multiple messages with incrementing delay
    Input Credentials
    Wait For Page To Load
    Create Message    Lucas Kean
    FOR    ${index}    IN RANGE    1    4
        Send Message    Hey, this is message No. ${index} from Robot
        Sleep    ${index}s
    END


Test Case 4: Dummy User Searches for #Uprise_CICT Posts
    [Documentation]    Dummy user searches for #Uprise_CICT posts from the year 2022
    Input Credentials
    Wait For Page To Load
    Perform Search

*** Keywords ***
Input Credentials
    Input Text    id=email    kean.lucas.v@bulsu.edu.ph
    Input Text    id=pass    retorika55
    Click Button    name=login
    Wait Until Element Is Visible    css=div[aria-label="Create a post"]    10s

Wait For Page To Load
    Wait Until Page Contains    Home    10s

Post Status
    Wait Until Element Is Visible    xpath=//div[@class="xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe"]    10s
    Click Element    xpath=//div[@class="xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe"]
    Wait Until Element Is Visible    css=div[contenteditable="true"]    10s  
    Input Text    css=div[contenteditable="true"]    I used Robot Framework in posting this status. I am doing a sample test automation. @lucas kean 4DG2 #SIA2
    Wait Until Element Is Visible    css=div[aria-label="Tag people"]    10s
    Click Element    css=div[aria-label="Tag people"]
    Wait Until Element Is Visible    css=li[aria-selected="false"]    10s
    Click Element    css=li[aria-selected="false"]
    Click Element    css=div[aria-label="Back"]
    Click Element    css=div[aria-label="Save Changes"]
    Click Element    css=div[aria-label="Post"]

Create Message
    [Arguments]    ${message_to}
    Click Element    css=div[aria-label="New message"] 
    Wait Until Element Is Visible    css=input[aria-label="Send message to"]    10s
    Input Text    css=input[aria-label="Send message to"]    ${message_to}
    Wait Until Element Is Visible    css=li[aria-selected="false"]    10s
    Click Element    css=li[aria-selected="false"]

Send Message
    [Arguments]    ${message}
    Click Element    css=div[aria-label="Message"]
    Input Text    css=div[aria-label="Message"]    ${message}
    Click Element    css=div[aria-label="Press enter to send"]

Perform Search
    Click Element    css=input[placeholder="Search Facebook"]
    Input Text    css=input[placeholder="Search Facebook"]    \#Uprise CICT
    Press Key    css=input[placeholder="Search Facebook"]     \\13
    Wait Until Element Is Visible    css=div[aria-label="Search results"]    10s
    Click Element    xpath=//div[2]/div/a/div/div[2]/div
    Wait Until Element Is Visible    xpath=//div[3]/div/div/div/div/div/span/span
    Click Element    xpath=//div[3]/div/div/div/div/div/span/span
    Wait Until Element Is Visible    xpath=//div[4]/div/div/div/span
    Click Element    xpath=//div[4]/div/div/div/span
    Wait Until Element Is Visible    css=div[aria-label="Search results"]    10s
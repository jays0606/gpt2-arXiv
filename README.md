# GPT2-marketing-man

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/fpem123/GPT2-marketing-man?branch=main)

This project generate marketing man style text using GPT-2 model.

model: [laxya007/gpt2_Marketingman](https://huggingface.co/laxya007/gpt2_Marketingman)

## how to use

* First, Choose wanna type!

* Second, Fill text in "text"! This will be base of marketing man style text!

* And then, Fill number in "samples"! The app generates sample number of text!

* If you select 'long' type, be fill number in "length"! The app generates text of that size


### ** Post parameter **

#### /GPT2-marketing-man/short


    text: The base text to generate a word.
    samples: How many generate word?
  


#### /GPT2-marketing-man/long


    text: The base text to generate marketing man style text.
    samples: How many generate text?
    length: Size of text.


### Output format

#### /GPT2-marketing-man/short

    {
        number: word,
        number: word,
        number: word,
        ...
    }
  

#### /GPT2-marketing-man/long

    {
        number: generated text,
        number: generated text,
        number: generated text,
        ...
    }
  

### ** With CLI **

#### /GPT2-marketing-man/short

Input example

    curl -X POST "https://main-gpt2-marketing-man-fpem123.endpoint.ainize.ai/GPT2-marketing-man/short" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=Hello " -F "samples=3"


Output example

    {
        "0": ",",
        "1": " for",
        "2": " Bit"
    }


#### /GPT2-marketing-man/long

Input example

    curl -X POST "https://main-gpt2-marketing-man-fpem123.endpoint.ainize.ai/GPT2-marketing-man/long" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=Hello, " -F "samples=3" -F "length=50"


Output example

    {
        "0": "Hello, world! Welcome to The Daily Apple! When I first started blogging, my first thought was, “Wow, I could actually do this.” In 2007, with the help of my daughter, I launched The Daily Apple website. As a",
        "1": "Hello, welcome to The Sims.  : Defining and Measuring Service Quality 309 Copyright 2010 Cengage Learning. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third",
        "2": "Hello, this is Mr. Clausen. This is my wife. I see that you are well aware that the airline reservation system is extremely difficult for the average consumer to use. I have thought about it, and after some discussion it seemed to me that perhaps"
    }
  

### ** With swagger **

Use API page: [Ainize](https://ainize.ai/fpem123/GPT2-marketing-man?branch=main)

### ** With demo **

Use demo page: [End point](https://main-gpt2-marketing-man-fpem123.endpoint.ainize.ai/)

--

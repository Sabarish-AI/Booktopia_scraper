<<<<<<<< PLEASE READ THIS COMPLETELY BEFORE RUNNING THE SCRIPT >>>>>>>><br>
---> This scraper is specially built for the Booktopia website to scrape its contents.<br>
----> It is developed in python along with the pychrome library.<br>
----> The booktopia website consists of the PerimeterX bot defender which prevents the scraping activities on the website.<br>
----> It is very important to bypass this PerimeterX bot defender to gain access to the website's contents.<br>
----> I have used an approach here where a chrome profile is created and launched using the pychrome library.<br>
----> The reason I have created a browser profile in chrome and launched is that the PerimeterX bot defender considers
      this to be a real user and whitelists the browser profile and ip address.<br>
----> On the initial run, we'll be prompted with a PerimeterX captcha of press and hold to authenticate if it is a real user.<br>
----> We have to manually solve this captch once to whitelist our browser profile and our IP.<br>
----> After solving this captcha once, we won't be prompted with a captcha thereafter as our browser profile and IP has been whitelisted by PerimeterX.<br>
----> I have also not used any requests, as it may trigger the bot defender.<br>
----> I have directly extracted the page source using tab.Runtime.evaluate(expression="""window.document.body.innerHTML""").<br>
----> Each run saves it in our local as offline.html.<br>
----> Once the html page source is saved offline in local, we are good to perform the scraping.<br>
----> I have also added click operations to navigate between the different book types.<br>
----> I have taken 20 random inputs here for testing.<br>
----> The results are stored in the results.csv

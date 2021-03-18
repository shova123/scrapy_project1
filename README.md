# database
<h1> Getting Started</h1>
<p>This repo is helpful in scrapping data from  studyinaustralia.gov.au, fetch data of all institutions , branches and courses</p>

<h2>Technical Requirement</h2>
<p>This project is built  on python framework called scrapy.Basic Knowledge of python3 and dom transverse is good to go to implement scrapy.
official site of scrapy is</p> <a href='https://docs.scrapy.org/en/latest/intro/overview.html'>Here</a>
<p>other requirements includes crawlera for ip rotation or proxy. Details in site https://www.scrapinghub.com/</p>. Scrapy project requires api key in settings.py file.
<p>Apache2 and For database MySql is used.</p>

<h2>Installation</h2>
   1)Python3 and pip3 is required to install scrapy 
   2)scrapy global setup is required for running project
   3)Apache2 installation
   4)Mysql installation
   
 <h2>How project works</h2>
   <ul>
     <li><p>Clone repo on local machine after all the required installations and setup</p></li>
     <li><p>enter inside the project directory</p></li>
     <li><p>run project using command "scrapy crawl australia"
  this command will call file australia.py and execute the site. all logs and scraped information can be viewed in  terminal </p></li>
   <li><p>All scrapped data will be saved in database called scrap.</p></li>
   </ul>
 
  
  
  

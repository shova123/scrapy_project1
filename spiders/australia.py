import scrapy
import regex
import mysql.connector
import sys, os

class AustraliaSpider(scrapy.Spider):
    name = 'australia'
    global db_connection
    global university_lastid
    db_connection = None
    allowed_domains = ['search.studyinaustralia.gov.au/course/search-results.html']
    start_urls = ['https://search.studyinaustralia.gov.au/course/search-results.html']
    user_agents = [
                    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
                    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
                    "Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.2.15 Version/10.00"   
    ]
    db_connection = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        passwd="Mt3ch@!@#",
                        database="australia"
                    )

    

    
    
    handle_httpstatus_list = [404]
    IELTS_score = 0
    PTE_score = 0
    TOEFL_score = 0
    TOEFL = 0 

    def parse(self, response):
        content = response.css("h2.univ_tit > a::attr(href)").extract()
        unicount=2
        for title in content:
            url = title
            detail_url = response.urljoin(url)
            yield scrapy.Request(url=detail_url, callback=self.uni_parse_detail, dont_filter=True)
               
       
        #follow agination link   
           
        #next_page_url = "https://search.studyinaustralia.gov.au/course/search-results.html" #+str(unicount)
        next_page_url =response.css("li.nxt > a::attr(href)").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
                


    def uni_parse_detail(self, response):

        global mycursor
        global university_lastid
        mycursor = db_connection.cursor()
   
        title = response.css("h1.cd_hd::text").extract_first()
        code = response.css("p.mt10 > span::text").extract_first()
        institution = response.css("p.crs_cd > span::text")[1].extract()
        institution_type = self.institution_type(institution)
        about = response.css(".cr_mid p::text").extract_first()
        logo = response.css("img.lazy-loaded::attr('src')").extract_first()
        link =''
        course_link = response.urljoin(response.css(".enq > a::attr('href')")[0].extract())
        uni_links =response.css(".enq > a::attr('href')").extract()
        uni_link_text = response.css(".enq > a::text").extract()
        if "Visit website" in uni_link_text:
            uni_link_index = uni_link_text.index("Visit website")
            link = uni_links[uni_link_index]
        
        uni_info ={
            'title':title,
            'code':code,
            'institution_type':institution_type,
            'about':about,
            'institute_email':'',
            'institute_contact':'',
            'logo':logo,
            'link':link,

        }
        add_uni = ("INSERT INTO university "
              "(university_name, about, code, institution_type, image, website_link) "
              "VALUES (%(title)s, %(about)s, %(code)s, %(institution_type)s,%(logo)s,%(link)s)")
           
        mycursor.execute(add_uni, uni_info)
        address1=response.css("address > div::text").extract()
        
        campus =response.css("address > div > strong::text").extract()
        add=[x.replace("\n",'') for x in address1]
        add=list(filter(None,add))

        address_len = len(add)
        add_count = 0  
        slist =[]
        sdata =[]
        for x in add:
            
            if((x.find("Australia") ==-1)):
                
                slist.append(x)
                

            else:
                if len(x) >10:
                    
                    slist.append(x)
                else:
                    slist.append(x)
                    sdata.append(slist)
                    slist =[]
                    
           
        
        
        self.log(sdata) 
        for data in sdata:
            
            if len(data)>3:
                institution_type = data[0]
                street1 =  data[1]
                address =  data[2]
                country =  data[3]
            else:
                institution_type =  campus[add_count]
                street1 =  data[0]
                address =  data[1]
                country =  data[2]
            add_count=add_count+1
            address_info = {
                    'title' :title,
                    'institution_type' : institution_type,
                    'street1' : street1,
                    'street2' : "",
                    'address' : address,
                    'country' : country
            }
            yield address_info

            
            add_address = ("INSERT INTO address "
                "(university_name, institution_name, street1, street2, address, country) "
                "VALUES (%(title)s, %(institution_type)s, %(street1)s, %(street2)s,%(address)s,%(country)s)")
            
            mycursor.execute(add_address, address_info)
            
        db_connection.commit()
        
        #yield scrapy.Request(url=course_link, callback=self.course_parse, dont_filter=True)
        
    def course_parse(self, response):
        course_link_detail = response.css("h3.crs_tit.univ_tit > a::attr('href')").extract()
        for link in course_link_detail:
            course_detail_url =response.urljoin(link)
            yield scrapy.Request(url=course_detail_url, callback=self.course_detail, dont_filter=True)
            
        #follow pagination link    
        next_page_url = response.css("li.nxt > a::attr(href)").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.course_parse, dont_filter=True)
       
            
        
    def course_detail(self, response):
        IELTS_score = 0
        PTE_score = 0
        TOEFL_PBT_score = 0
        TOEFL_IBT_score = 0
        TOEFL = 0
        ISLPR_score = 0
        CAMBRIDGE_score = 0
        fee = ''
        fee1 = ''
        start_date = ''
        start_date1= ''
        duration = ''
        duration1 = ''
        study_mode = ''
        study_mode1 = ''
        address = ''
        address1 = ''
        branch=''
        branch1=''
        count = 0
        entry_criteria =''
        description =''

        months = {"January" : "Jan",
            "February"    : "Feb",
            "March"  : "Mar",
            "April"  :  "Apr",
            "May"    :  "May",
            "June"     : "Jun",
            "July"      : "Jul",
            "August"    : "Aug",
            "September":"Sep",
            "October"   : "Oct",
            "November"  : "Nov",
            "December"  : "Dec"}
            


        course_title = response.css("h1.cd_hd::text").extract_first()
        uni_title = response.css("h2.lnk_hrd > a::text").extract_first()

        description_list = response.css(".cr_mid > p::text").extract()
        for d in description_list:
            description = description +" " +d

        entry_criteria_list = response.xpath('//div[@class="fl w100p"]//text()').extract()
        for e in entry_criteria_list:
            entry_criteria = entry_criteria +" " +e

        ##############Check if code and institution firld is available##############   
        if(len(response.css("div.cr_mid > p.crs_txt::text").extract())>=2):
            code = response.css("div.cr_mid > p.crs_txt::text")[0].extract()
            institution_tye = response.css("div.cr_mid > p.crs_txt::text")[1].extract()
        else:
            code = ''
            institution_tye=response.css("div.cr_mid > p.crs_txt::text")[0].extract()

        
        criteria = response.css(".fl >p::text").extract()
        
        
        for cri in criteria:
            NumericPattern = '\d+'
            if("IELTS" in cri):
                IELTS = cri[cri.find("IELTS"):-1]
                IELTS_score  = regex.findall(NumericPattern,IELTS)
                if (len(IELTS_score)>0):
                        IELTS_score =IELTS_score[0]
                else:
                        IELTS_score=0
            if("PTE" in cri):
                PTE = cri[cri.find("PTE"):-1]
                PTE_score  = regex.findall(NumericPattern,PTE)
                if (len(PTE_score)>0):
                        PTE_score =PTE_score[0]
                else:
                        PTE_score=0
            if("ISLPR" in cri):
                ISLPR = cri[cri.find("ISLPR"):-1]
                ISLPR_score  = regex.findall(NumericPattern,ISLPR)
                if (len(ISLPR_score)>0):
                        ISLPR_score =ISLPR_score[0]
                else:
                        ISLPR_score=0
            if("CAMBRIDGE" in cri):
                CAMBRIDGE = cri[cri.find("CAMBRIDGE"):-1]
                CAMBRIDGE_score  = regex.findall(NumericPattern,CAMBRIDGE)
                if (len(CAMBRIDGE_score)>0):
                        CAMBRIDGE_score =CAMBRIDGE_score[0]
                else:
                        CAMBRIDGE_score=0
            if("TOEFL" in cri):
                TOEFL = cri[cri.find("TOEFL"):-1]
                if(("IBT" in TOEFL) or ("internet" in TOEFL)):
                     if("IBT" in TOEFL):
                        StrPosVal = 'IBT'
                     elif("internet" in TOEFL):
                        StrPosVal = 'internet'
                     
                     IBT = TOEFL[TOEFL.find(StrPosVal):-1]
                         
                     TOEFL_IBT_score = regex.findall(NumericPattern, IBT)
                     if (len(TOEFL_IBT_score)>0):
                        TOEFL_IBT_score =TOEFL_IBT_score[0]
                     else:
                         
                        TOEFL_IBT_score=0

                         
                if(("PBT" in TOEFL) or ("paper" in TOEFL)):
                     if("PBT" in TOEFL):
                         StrPosVal = 'PBT'
                     elif("paper" in TOEFL):
                        StrPosVal = 'paper'
                     PBT = TOEFL[TOEFL.find(StrPosVal):-1]
                     TOEFL_PBT_score = regex.findall(NumericPattern, PBT)
                     self.log(TOEFL_PBT_score)
                     if (len(TOEFL_PBT_score)>0):
                         TOEFL_PBT_score = TOEFL_PBT_score[0]
                     else:
                         
                        TOEFL_PBT_score=0

        no_of_oppurtunity= len(response.css("div.fl_w100 > .rs_cnt").extract())
        
        oppurtunity = response.css("div.tb_cl > .fl_w100 > span::text").extract()
        oppurtunity = [x.replace("\n",'') for x in oppurtunity]
        oppurtunity = list(filter(None,oppurtunity))

        #############Check oppurtunity fields Tution fees, Duration,Study mode, Start Date###################
        no_of_oppurtunity_field = int(len(response.css("div.tb_cl > .fl_w100").extract())/no_of_oppurtunity)
        
        
        if no_of_oppurtunity_field ==2:
            tution_fees1 = response.css("div.tb_cl > .fl_w100:nth-child(1) > span::text").extract()
            tution_fees1 = [x.replace("\n",'') for x in tution_fees1]
            tution_fees1 = list(filter(None,tution_fees1))

            duration1    = response.css("div.tb_cl > .fl_w100:nth-child(2) > span::text").extract()
            duration1 = [x.replace("\n",'') for x in duration1]
            duration1 = list(filter(None,duration1))
            


        elif no_of_oppurtunity_field ==3:
            tution_fees1 = response.css("div.tb_cl > .fl_w100:nth-child(1) > span::text").extract()
            tution_fees1 = [x.replace("\n",'') for x in tution_fees1]
            tution_fees1 = list(filter(None,tution_fees1))

            opp1 = response.css("div.tb_cl > .fl_w100:nth-child(2) > span::text").extract()
            opp1 = [x.replace("\n",'') for x in opp1]
            opp1 = list(filter(None,opp1))

           
            if 'Start date:' in opp1:
                start_date1 =  list(filter(None,opp1))
            if 'Duration:' in opp1:
                duration1 =  list(filter(None,opp1))
  
            opp2  = response.css("div.tb_cl > .fl_w100:nth-child(3) > span::text").extract()
            opp2 = [x.replace("\n",'') for x in opp2]
            opp2 = list(filter(None,opp2))

            if 'Study mode:' in opp2:
                study_mode1 = list(filter(None,opp2))
            if 'Duration:' in opp2:
                duration1 = list(filter(None,opp2))

            

        else:

            tution_fees1 = response.css("div.tb_cl > .fl_w100:nth-child(1) > span::text").extract()
            tution_fees1 = [x.replace("\n",'') for x in tution_fees1]
            tution_fees1 = list(filter(None,tution_fees1))

            duration1    = response.css("div.tb_cl > .fl_w100:nth-child(3) > span::text").extract()
            duration1 = [x.replace("\n",'') for x in duration1]
            duration1 = list(filter(None,duration1))

            study_mode1  = response.css("div.tb_cl > .fl_w100:nth-child(4) > span::text").extract()
            study_mode1 = [x.replace("\n",'') for x in study_mode1]
            study_mode1 = list(filter(None,study_mode1))

            start_date1  = response.css("div.tb_cl > .fl_w100:nth-child(2) > span::text").extract()
            start_date1 = [x.replace("\n",'') for x in start_date1]
            start_date1 = list(filter(None,start_date1))

       

       ######################Get three form  of  months example Jan,feb,Mar etc#############
        slist =''
        sdata = []
        start_date1_len = (len(start_date1)-1)
        opp_count = 0    
        
        if len(start_date1) >0:
            for x in start_date1:
                
                
                if(x.find("Start") ==-1):
                    
                    if(len(x.split()) >2) :
                        xkey = x.split()[1] 
                        self.log(xkey)
                        if xkey in months: 
                            x=months[x.split()[1]]
                        else:
                            x = x
                    elif(len(x.split()) ==2) :
                        xkey = x.split()[0]
                        self.log(xkey)
                        if xkey in months: 
                            x=months[x.split()[0]]
                        else:
                            x = x
                    else:
                        x = x
                    if slist:
                        slist = slist+' , ' +x
                    else:
                        slist = x
                    if(opp_count==start_date1_len):
                        
                        sdata.append(slist)
                            
                else:
                    if slist:
                        sdata.append(slist)
                                    
                    slist = ''
                opp_count = opp_count +1
                    
        branch1=response.css("p.vn_adrs > strong::text").extract()
        address1=response.css("address.ovnus > div::text").extract()
        add=[x.replace("\n",'') for x in address1]
        add=list(filter(None,add))

        ##############################Fetch List of Oppurtunity################
        while(count < no_of_oppurtunity):
            self.log(duration1)
            oppurtunity = response.css("div.fl_w100 > .rs_cnt")[count].extract()  
            oppurtunity = [x.replace("\n",'') for x in oppurtunity]
            oppurtunity = list(filter(None,oppurtunity))   
            if count ==0:
                
                branch = branch1[0]
                address = add[0]+' ,'+add[1]
                
                if 'Per Year' in tution_fees1[1]:  
                    fee     = tution_fees1[1].split()[0]              
                    if len(tution_fees1[1].split())==3:
                        installment = tution_fees1[1].split()[1] + " "+ tution_fees1[1].split()[2]
                    elif len(tution_fees1[1].split())==4:
                        installment = tution_fees1[1].split()[0] + " "+ tution_fees1[1].split()[1]+ " "+ tution_fees1[1].split()[2]+ " "+ tution_fees1[1].split()[3]
                    
                    else:
                        installment = tution_fees1[1].split()[1] + " "+ tution_fees1[1].split()[2]+ " "+ tution_fees1[1].split()[3]+ " "+ tution_fees1[1].split()[4]
                else:
                    fee = tution_fees1[1]
                    installment =''
                if duration1:
                    if  'years' in duration1[1] or 'year' in duration1[1]:  


                        if duration1[1].find(" or ")== -1:
                            duration = duration1[1].split()
                            
                        else:
                            
                            duration = duration1[1].split('or')
                            duration_count = len(duration)
                            if duration_count>2:
                                duration = duration[duration_count-1]
                                duration = duration.split()
                            else:
                                duration = duration[1]
                                duration = duration.split()
                        if ("Variable" in duration1) or ("Minimum of 24 units" in duration1) or ("Flexible" in duration1):
                            duration = duration1[1]
                        elif  'years' in duration[1] or 'year' in duration[1]:  
                            if self.is_int_or_float(duration[0])==2:
                                duration = self.Float_years_and_months(duration[0])
                            elif type(duration[0]) ==int:
                                    duration = self.Years_and_months(duration[0])
                            else:
                                    duration = duration[0]
                    else:
                            duration = duration1[1]

                if study_mode1:
                    study_mode = study_mode1[1]
                if sdata:
                    start_date = sdata[0].lstrip(',')
                
                    

            if count ==1:
                    branch = branch1[1]
                    address = add[3]+' ,'+add[4]
                    if 'Per Year' in tution_fees1[3]: 
                        fee     = tution_fees1[3].split()[0]
                        
                        if len(tution_fees1[3].split())==3:
                            installment = tution_fees1[3].split()[1] + " "+ tution_fees1[3].split()[2]
                        elif len(tution_fees1[3].split())==4:
                            installment = tution_fees1[3].split()[0] + " "+ tution_fees1[3].split()[1]+ " "+ tution_fees1[3].split()[2]+ " "+ tution_fees1[3].split()[3]
                    
                        else:
                            installment = tution_fees1[3].split()[1] + " "+ tution_fees1[3].split()[2]+ " "+ tution_fees1[3].split()[3]+ " "+ tution_fees1[3].split()[4]
                    else :
                        fee     = tution_fees1[3]
                        installment = ''

                    if duration1:
                        if  'years' in duration1[3] or 'year' in duration1[3]:  

                            if duration1[3].find("or")== -1:
                                duration = duration1[3].split()
                            
                            else:
                                duration = duration1[3].split('or')
                                duration_count = len(duration)
                                if duration_count>2:
                                    duration = duration[duration_count-1]
                                    duration = duration.split()
                                else:
                                    duration = duration[1]
                                    duration = duration.split()
                            self.log(duration)
                            if ("Variable" in duration1) or ("Minimum of 24 units" in duration1):
                                duration = duration1[3]
                            elif  'years' in duration[1] or 'year' in duration[1]:  
                                if self.is_int_or_float(duration[0])==2:
                                    duration = self.Float_years_and_months(duration[0])
                                elif type(duration[0]) ==int:
                                    duration = self.Years_and_months(duration[0])
                                else:
                                    duration = duration[0]
                        else:
                            duration = duration1[3]
                        
                    if study_mode1:
                        study_mode = study_mode1[3]
                    if len(sdata)>1:
                        start_date = sdata[1].lstrip(',')
                   
    

            if count ==2:
                    branch = branch1[2]
                    address = add[6] + ','+ add[7]
                    if 'Per Year' in tution_fees1[5]: 
                        fee     = tution_fees1[5].split()[0]
                        installment = tution_fees1[5].split()[1] + " "+ tution_fees1[5].split()[2]
                        if len(tution_fees1[5].split())==3:
                            installment = tution_fees1[5].split()[1] + " "+ tution_fees1[5].split()[2]
                        elif len(tution_fees1[5].split())==4:
                            installment = tution_fees1[5].split()[0] + " "+ tution_fees1[5].split()[1]+ " "+ tution_fees1[5].split()[2]+ " "+ tution_fees1[5].split()[3]
                
                        else:
                            installment = tution_fees1[5].split()[1] + " "+ tution_fees1[5].split()[2]+ " "+ tution_fees1[5].split()[3]+ " "+ tution_fees1[5].split()[4]
                
                    else :
                        fee     = tution_fees1[5]
                        installment = ''
                    
                    if duration1:
                        if  'years' in duration1[5] or 'year' in duration1[5]:  

                            if duration1[5].find("or")== -1:
                                duration = duration1[1].split()
                            
                            else:
                                duration = duration1[5].split('or')
                                duration_count = len(duration)
                                if duration_count>2:
                                    duration = duration[duration_count-1]
                                    duration = duration.split()
                                else:
                                    duration = duration[1]
                                    duration = duration.split()
                            if ("Variable" in duration1) or ("Minimum of 24 units" in duration1):
                                duration = duration1[5]
                            elif  'years' in duration[1] or 'year' in duration[1]:  
                                if self.is_int_or_float(duration[0])==2:
                                    duration = self.Float_years_and_months(duration[0])
                                elif type(duration[0]) ==int:
                                    duration = self.Years_and_months(duration[0])
                                else:
                                    duration = duration[0]
                        else:
                            duration = duration1[5]
                    
                    if study_mode1:
                        study_mode = study_mode1[5]
                    if len(sdata)>2:
                        start_date = sdata[2].lstrip(',')
                    
                   
                       
            if count ==3:
                    branch = branch1[3]
                    address = add[9] + ','+ add[10]
                    if 'Per Year' in tution_fees1[7]: 
                        fee     = tution_fees1[7].split()[0]
                        if len(tution_fees1[7].split())==3:
                            installment = tution_fees1[7].split()[1] + " "+ tution_fees1[7].split()[2]
                        elif len(tution_fees1[7].split())==4:
                            installment = tution_fees1[7].split()[0] + " "+ tution_fees1[7].split()[1]+ " "+ tution_fees1[7].split()[2]+ " "+ tution_fees1[7].split()[3]
                    
                        else:
                            installment = tution_fees1[7].split()[1] + " "+ tution_fees1[7].split()[2]+ " "+ tution_fees1[7].split()[3]+ " "+ tution_fees1[7].split()[4]
                
                    else:
                        fee     = tution_fees1[7]
                        installment = ''

                    
                    if duration1:
                        if  'years' in duration1[1] or 'year' in duration1[1]:  

                            if duration1[7].find("or")== -1:
                                duration = duration1[7].split()
                            
                            else:
                                duration = duration1[7].split('or')
                                duration_count = len(duration)
                                if duration_count>2:
                                    duration = duration[duration_count-1]
                                    duration = duration.split()
                                else:
                                    duration = duration[1]
                                    duration = duration.split()
                            if ("Variable" in duration1) or ("Minimum of 24 units" in duration1):
                                duration = duration1[7]
                            elif  'years' in duration[1] or 'year' in duration[1]:  
                                if self.is_int_or_float(duration[0])==2:
                                    duration = self.Float_years_and_months(duration[0])
                                elif type(duration[0]) ==int:
                                    duration = self.Years_and_months(duration[0])
                                else:
                                    duration = duration[0]
                        else:
                            duration = duration1[7]
                    

                    if study_mode1:
                        study_mode = study_mode1[7]
                    if len(sdata)>3:
                        start_date = sdata[3].lstrip(',')
                    
            
                    
                       
            count = count + 1
              
                                 
            course_info={ 
                'university_lastid':university_lastid,
                'university_title':uni_title,
                'course_title':course_title,
                'code':code,
                'institution_type':institution_tye,
                'fee':fee,
                'start_date':start_date,
                'installment':installment,
                'duration':duration,
                'study_mode':study_mode,
                'address':address,
                'branch':branch,
                'ielts_score':IELTS_score,
                'pte':PTE_score,
                'toefl_ibt':TOEFL_IBT_score,
                'toefl_pbt':TOEFL_PBT_score,
                "islpr_score":ISLPR_score,
                "cambridge_score":CAMBRIDGE_score
            }
            #############Save course in database############
            global mycursor
            mycursor = db_connection.cursor()
   
            add_course = ("INSERT INTO course "
              "(university_id,university_title, course_title, code, institution_type, fee,installment, intake, duration, study_mode, address, branch,entry_criteria, ielts_score, pte, tofel_ibt, tofel_pbt, islpr_score, cambridge_score) "
              "VALUES (%s,%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )")
            args = (university_lastid, uni_title,course_title,code,institution_tye,fee,installment,start_date,duration,study_mode,address,branch,entry_criteria,IELTS_score,PTE_score,TOEFL_IBT_score,TOEFL_PBT_score,ISLPR_score,CAMBRIDGE_score)
            mycursor.execute(add_course, args)
            
            db_connection.commit()
            lastid=mycursor.lastrowid

            yield course_info

    def Float_years_and_months(self,param_year):
        year = param_year
        year = year.split('.')
        months = (int(year[0]) * 12)+int(year[1])
        months = str(months) + " month(s)"

        return months

    def Years_and_months(self,param_year):
        year = int(param_year)
        months = year*12
        months = str(months) + " month(s)"

        return months

    def is_int_or_float(self,s):
   
        try:
            float(s)

            return 1 if s.count('.')==0 else 2
        except ValueError:
            return -1

    ############### Define Institution type ###############
    def institution_type(self,university_name):
        if 'University' in university_name:
            institution_name = 'University' 
        elif 'schools' in university_name:
            institution_name = 'School' 
        elif 'Institute' in university_name:
            institution_name = 'Institute' 
        elif 'College' in university_name:
            institution_name = 'College' 
        elif 'Campus' in university_name:
            institution_name = 'Campus' 
        elif 'Training' in university_name:
            institution_name = 'Training Centre' 
        elif 'Diploma' in university_name:
            institution_name = 'Diploma' 
        elif 'Academy' in university_name:
            institution_name = 'Academy' 
        elif 'English' in university_name:
            institution_name = 'language training' 
        elif 'Centre' in university_name:
            institution_name = 'language training'
        else:
            institution_name = 'Training Centre'
        return institution_name

            

        
        
        

import requests
import pandas as pd
import gc, time
from check_n_get_info.web_check_n_get_info import WebRequestHandler, process_multiple_urls
from analyze_html_by_LLM.analyze_html_by_EEVE import HTMLAnalyzerBot, analyze_html



if __name__ == "__main__" :

    

# =================================================
# 
# 접속 가능한 사이트인지 체크
# 
# =================================================
    # df = pd.read_csv("C:/Users/COM/VscodeProject/Crawling_n_Analyze_by_EEVE/data/Enterprise_url_from_GDWEB.csv")
    
    # urls = df.iloc[:,1].to_list()

    # # 테스트용 test_urls
    # # test_urls = [
    # #     "https://www.moguchon.co.kr/wn/",
    # #     "https://flip.dorelan.co.kr",
    # #     "https://www.google.com"
    # # ]

    # results = process_multiple_urls(urls)

    # Usable_urls = []
    
    # for url, ok_or_not in results.items():
    #     if ok_or_not == "Usable":
    #         Usable_urls.append(url)
           
    # save_urls = pd.DataFrame(Usable_urls)
    # save_urls.to_csv("C:/Users/COM/VscodeProject/Crawling_n_Analyze_by_EEVE/data/checked_urls.csv", encoding="utf-8-sig", header=False, index=False)
    
    # print("save checked urls!")

# =================================================
# 
# url 리스트를 들어가서 하나씩 분석석
# 
# =================================================

    resting_time = 120

    df = pd.read_csv("C:/Users/COM/VscodeProject/Crawling_n_Analyze_by_EEVE/data/checked_urls.csv")

    for temp_num in range(1,11):

        Usable_urls = df.iloc[1:2,0].to_list()
        
        limit_html_len = 50000
        
        for Usable_url in Usable_urls:
                
            # 실행
            result_list = []
            
            result_of_LLM, clean_html_len = analyze_html(Usable_url, limit_html_len)
            
            print("type(result_of_LLM) : ", type(result_of_LLM))
            print("len(result_of_LLM) : ", len(result_of_LLM))
            
            result_list.append([Usable_url, result_of_LLM, clean_html_len, limit_html_len])
            
        result_df = pd.DataFrame(data=result_list, columns=['url', 'Analyze_Content','Original_len', 'Cutted_len'])
        
        result_df.to_csv(f"C:/Users/Dolphinnn/VscodeProjects/Crawling_n_Analyze_by_EEVE/data/analyze_result_{temp_num}.csv", encoding="utf-8-sig")
        
        print("Result is saved!!")
        
        gc.collect()
        print("gc.collect is working!!")
        
        time.sleep(resting_time)
        print("resting is Done, Let's work!!")
    
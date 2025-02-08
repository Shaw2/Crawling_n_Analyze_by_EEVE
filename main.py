import requests
import pandas as pd

from check_n_get_info.web_check_n_get_info import WebRequestHandler, process_multiple_urls
from analyze_html_by_LLM.analyze_html_by_EEVE import HTMLAnalyzerBot, clean_html, analyze_html



if __name__ == "__main__" :

    df = pd.read_csv("C:/Users/COM/VscodeProject/Crawling_n_Analyze_by_EEVE/data/Enterprise_url_from_GDWEB.csv")
    
    urls = df.iloc[:,1].to_list()

    # 테스트용 test_urls
    # test_urls = [
    #     "https://www.moguchon.co.kr/wn/",
    #     "https://flip.dorelan.co.kr",
    #     "https://www.google.com"
    # ]

    results = process_multiple_urls(urls)

    Usable_urls = []
    
    for url, ok_or_not in results.items():
        if ok_or_not == "Usable":
            Usable_urls.append(url)
           
    save_urls = pd.DataFrame(Usable_urls)
    save_urls.to_csv("C:/Users/COM/VscodeProject/Crawling_n_Analyze_by_EEVE/data/checked_urls.csv", encoding="utf-8-sig", header=False, index=False)
    
    print("save checked urls!")

    for Usable_url in Usable_urls:
        
    # # 테스트용 단일 URL
    # url = "https://google.com/"
    
        response = requests.get(Usable_url, verify=False)

        if response.status_code == 200:
            clean_content = clean_html(response.text)
            # print(clean_content)  # 정리된 HTML 출력
        else:
            print("페이지를 가져오지 못했습니다.")    
        
        # HTML 길이
        print("len(clean_content) : ", len(clean_content))        

        cutted_clean_content = clean_content[:50000]
        
        # 실행
        result_list = []
        
        result_of_LLM = analyze_html(cutted_clean_content)
        print("type(result_of_LLM) : ", type(result_of_LLM))
        print("len(result_of_LLM) : ", len(result_of_LLM))
        
        result_list.append([Usable_url, result_of_LLM, len(clean_content), len(cutted_clean_content)])
        
    result_df = pd.DataFrame(data=result_list, columns=['url', 'Analyze_Content','Original_len', 'Cutted_len'])
    
    result_df.to_csv("C:/Users/COM/VscodeProject/Crawling_n_Analyze_by_EEVE/data/analyze_result.csv", encoding="utf-8-sig")
    print("Result is saved!!")
    
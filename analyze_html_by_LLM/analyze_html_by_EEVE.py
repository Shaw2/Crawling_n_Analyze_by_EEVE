
import requests
from bs4 import BeautifulSoup
import ollama
from typing import List, Dict
import logging

import textwrap
import re
import asyncio


# def clean_html(html):
#     """필요 없는 태그를 제거하는 함수"""
#     soup = BeautifulSoup(html, "html.parser")

#     # 제거할 태그 목록
#     remove_tags = ["script", "style", "meta", "link", "iframe", "embed", "object", "noscript"]

#     for tag in soup.find_all(remove_tags):
#         tag.decompose()  # 해당 태그 제거

#     return soup.prettify()

# class HTMLAnalyzerBot:
#     def __init__(self, model_name: str = "DS_Q4_K_M:v1", chunk_size: int = 4000):
#         """
#         HTML 분석을 위한 챗봇 초기화
        
#         Args:
#             model_name (str): 사용할 Ollama 모델 이름
#             chunk_size (int): HTML 청크의 최대 크기
#         """
#         self.model = model_name
#         self.chunk_size = chunk_size
#         self.chunks: List[str] = []
#         self.current_context = ""
        
#     def chunk_html(self, html_content: str) -> List[str]:
#         """
#         HTML을 청크로 분할
        
#         Args:
#             html_content (str): 분석할 HTML 내용
            
#         Returns:
#             List[str]: HTML 청크 리스트
#         """
#         # BeautifulSoup을 사용하여 HTML 파싱
#         soup = BeautifulSoup(html_content, 'html.parser')
        
#         # 의미 있는 단위로 분할 (예: div, section, article 등)
#         meaningful_tags = ['div', 'section', 'article', 'main', 'header', 'footer']
#         sections = []
        
#         for tag in meaningful_tags:
#             elements = soup.find_all(tag)
#             for element in elements:
#                 sections.append(str(element))
        
#         # 청크로 나누기
#         chunks = []
#         current_chunk = ""
        
#         for section in sections:
#             if len(current_chunk) + len(section) < self.chunk_size:
#                 current_chunk += section
#             else:
#                 if current_chunk:
#                     chunks.append(current_chunk)
#                 current_chunk = section
        
#         if current_chunk:
#             chunks.append(current_chunk)
            
#         self.chunks = chunks
#         return chunks
    
#     def add_html_content(self, html_content: str):
#         """
#         HTML 내용을 추가하고 청킹 수행
        
#         Args:
#             html_content (str): 추가할 HTML 내용
#         """
#         self.chunks = self.chunk_html(html_content)
#         self.current_context = f"HTML 분석을 시작합니다. 총 {len(self.chunks)}개의 청크가 있습니다."
    
#     async def process_chunks(self) -> str:
#         """
#         모든 HTML 청크를 처리하고 분석
        
#         Returns:
#             str: 전체 HTML에 대한 분석 결과
#         """
#         messages = [
#             {
#                 "role": "system",
#                 "content": "당신은 HTML 코드를 분석하는 전문가입니다. 각 청크를 분석하고, 전체적인 구조와 주요 특징을 파악해주세요."
#             }
#         ]
        
#         # 각 청크 처리
#         for i, chunk in enumerate(self.chunks, 1):
#             messages.append({
#                 "role": "user",
#                 "content": f"청크 {i}/{len(self.chunks)}:\n{chunk}"
#             })
            
#             response = await ollama.chat(
#                 model=self.model,
#                 messages=messages
#             )
            
#             messages.append({
#                 "role": "assistant",
#                 "content": response['message']['content']
#             })
        
#         # 최종 분석 요청
#         messages.append({
#             "role": "user",
#             "content": "지금까지 분석한 모든 HTML 청크를 종합하여 전체적인 구조와 특징을 요약해주세요."
#         })
        
#         final_response = await ollama.chat(
#             model=self.model,
#             messages=messages
#         )
        
#         return final_response['message']['content']

# # 사용 예시
# async def analyze_html(html_content: str):
#     analyzer = HTMLAnalyzerBot()
#     analyzer.add_html_content(html_content)
#     result = await analyzer.process_chunks()
#     return result


# # 실행 코드
# if __name__ == "__main__":
#     import asyncio
    
#     # 테스트할 URL (예제)
#     url = "https://dlchemical.co.kr/"
#     response = requests.get(url)

#     if response.status_code == 200:
#         clean_content = clean_html(response.text)
#         print(clean_content)  # 정리된 HTML 출력
#     else:
#         print("페이지를 가져오지 못했습니다.")    
    
#     # 예시 HTML
#     html_example = clean_content
    
#     # 비동기로 실행
#     result = asyncio.run(analyze_html(html_example))
#     print(result)


class HTMLAnalyzerBot:
    def __init__(self, model_name: str = "EEVE_test:latest", chunk_size: int = 4000):
        """
        HTML 분석을 위한 챗봇 초기화
        
        Args:
            model_name (str): 사용할 Ollama 모델 이름
            chunk_size (int): HTML 청크의 최대 크기
        """
        self.model = model_name
        self.chunk_size = chunk_size
        self.chunks: List[str] = []
        self.current_context = ""
        
        # 로깅 설정
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            

    def clean_html_from_url(self, url):
        """필요 없는 태그를 제거하는 함수"""
        
        response = requests.get(url, verify=False)

        if response.status_code == 200:
        
            soup = BeautifulSoup(response.text, "html.parser")
            self.logger.info(f"현재 처리중 - {url}")
            
            # 제거할 태그 목록
            remove_tags = ["script", "style", "meta", "link", "iframe", "embed", "object", "noscript"]

            for tag in soup.find_all(remove_tags):
                tag.decompose()  # 해당 태그 제거

        else:
            print("페이지를 가져오지 못했습니다.")
            
        clean_content = soup.prettify()
        
        self.logger.info(f"len(clean_content) : {len(clean_content)}")
        return soup.prettify()

    def chunk_html(self, html_content: str) -> List[str]:
        """
        HTML을 청크로 분할
        
        Args:
            html_content (str): 분석할 HTML 내용
            
        Returns:
            List[str]: HTML 청크 리스트
        """
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # NOTE : 분할하는게 맞을까? 분할을 하게되면 흐름을 잃지 않으려나
        # 의미 있는 단위로 분할 (예: div, section, article 등)
        meaningful_tags = ['div', 'section', 'article', 'main', 'header', 'footer']
        sections = []
        
        for tag in meaningful_tags:
            # print("What is tag ? : ", tag)
            elements = soup.find_all(tag)
            # print("====================================")
            for element in elements:
                # print("What is element ? : ", element)
                sections.append(str(element))
        
        # 청크로 나누기
        chunks = []
        current_chunk = ""
        
        for section in sections:
            if len(current_chunk) + len(section) < self.chunk_size:
                current_chunk += section
            else:
                if current_chunk:
                    print("len(current_chunk) is appended in chunk : ", len(current_chunk))
                    chunks.append(current_chunk)
                current_chunk = section
        
        if current_chunk:
            chunks.append(current_chunk)
            
        self.chunks = chunks
        return chunks
    
    def add_html_content(self, html_content: str):
        """
        HTML 내용을 추가하고 청킹 수행
        
        Args:
            html_content (str): 추가할 HTML 내용
        """
        self.chunks = self.chunk_html(html_content)
        self.current_context = f"HTML 분석을 시작합니다. 총 {len(self.chunks)}개의 청크가 있습니다."
    
    def process_chunks(self) -> str:
        """
        모든 HTML 청크를 처리하고 분석
        
        Returns:
            str: 전체 HTML에 대한 분석 결과
        """
        messages = [
            {
                "role": "system",
                "content": "당신은 HTML 코드를 분석하는 전문가입니다. 각 청크를 분석하고, 전체적인 구조와 주요 특징을 파악해주세요."
            }
        ]
        
        # 각 청크 처리
        for i, chunk in enumerate(self.chunks, 1):
            messages.append({
                "role": "user",
                "content": f"청크 {i}/{len(self.chunks)}:\n{chunk}"
            })
            
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            
            messages.append({
                "role": "assistant",
                "content": response['message']['content']
            })
            
            self.logger.info(f"청크 {i}/{len(self.chunks)} 처리 완료")
        
        # 최종 분석 요청
        messages.append({
            "role": "user",
            "content": "지금까지 분석한 모든 HTML 청크를 종합하여 전체적인 구조와 특징을 요약해주세요."
        })
        
        final_response = ollama.chat(
            model=self.model,
            messages=messages
        )
        
        return final_response['message']['content']

def analyze_html(url: str):
    """
    HTML 분석 실행 함수
    
    Args:
        html_content (str): 분석할 HTML 내용
        
    Returns:
        str: 분석 결과
    """
    analyzer = HTMLAnalyzerBot()
    
    clean_html = analyzer.clean_html_from_url(url)
    analyzer.add_html_content(clean_html)
    
    # return None
    return analyzer.process_chunks()

# 실행 코드
if __name__ == "__main__":
    
    # 테스트할 URL (예제)
    url = "https://www.google.com/"
    
    
    # 실행
    result = analyze_html(url)
    print(result)